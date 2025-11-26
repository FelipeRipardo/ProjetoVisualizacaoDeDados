import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os

#Registra a página
dash.register_page(__name__, path = '/dashboard', name = 'Dashboard')

#Primeiro passo: Carregar os dados do arquivo .csv
caminho_arquivo = 'dados_limpos_microbiota.csv'

#Garante que o programa não trave caso o caminho do arquivo não seja encontrado, criando uma "tabela fantasma" através do DF
#e configurando os cabeçalhos corretamente
if os.path.exists(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo)
else:
    df = pd.DataFrame(columns = ['Phylum', 'Genus', 'Group', 'Abundance'])


#Segundo passo: Layout da página
layout = dbc.Container([
    dbc.Row([
        #Sidebar -> Filtros
        dbc.Col([
            html.H4("⚙️ Filtros", className = 'mb-4 text-primary'),

            html.Label("1 - Nível Taxonômico:", className = 'fw-bold'),
            dcc.Dropdown(
                id = 'tax-level-filter',
                options = [
                    {'label': 'Filo (Phylum) - Macro', 'value': 'Phylum'},
                    {'label': 'Gênero (Genos) - Detalhado', 'value': 'Genus'}
                ],
                value = 'Phylum',
                clearable = False,
                className = 'mb-3'
            ),

            html.Label("2 - Filtrar Bactéria Específica:", className = 'fw-bold'),
            dcc.Dropdown(
                id = 'bacteria-filter',
                placeholder = 'Selecione ou digite...',
                className = 'mb-3'
            ),

            html.Hr(),
            dbc.Alert([
                html.H6("Status: ", className = 'alert-heading'),
                html.P("3 Visualizações Ativas", className = 'mb-0 small fw-bold text-success'),
                html.P(f"Registros: {len(df):,}", className = 'mb-0 small')
            ], color = 'light'),
        ], width = 3, className = 'bg-white p-4 shadow-sm rounded'),

        #Área principal do projeto - Gráficos
        dbc.Col([
            html.H3("📊 Análise Comparativa", className = 'mb-4'),

            #Primeira linha e primeiro gráfico: Gráfico de Barras (Comparação)
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("1 - Média de Abundância (Comparação Direta)"),
                        dbc.CardBody(dcc.Graph(id = 'grafico-barras', style = {'height': '350px'}))
                    ], className = 'mb-4 shadow-sm')
                ], width = 12)
            ]),

            #Segunda linha: Dividida em dois gráficos menores
            dbc.Row([
                #Segundo gráfico: Boxplot (Distribuição)
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("2 - Distribuição e Outliers"),
                        dbc.CardBody(dcc.Graph(id = 'grafico-boxplot', style = {'height': '350px'}))
                    ], className = 'h-100 shadow-sm')
                ], width = 7),

                #Terceiro gráfico: Pizza (Composição)
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("3 - Representatividade (%)"),
                        dbc.CardBody(dcc.Graph(id = 'grafico-pizza', style = {'height': '350px'}))
                    ], className = 'h-100 shadow-sm')
                ], width = 5),
            ])
        ], width = 9),
    ])
], fluid = True, className = 'bg-light pt-4 min-vh-100')


#Terceiro passo: Callbacks

@callback(
    Output('bacteria-filter', 'options'),
    Output('bacteria-filter', 'value'),
    Input('tax-level-filter', 'value'),
)

def update_dropdown_options(tax_level):
    if df.empty: return[], None
    opcoes = sorted(df[tax_level].dropna().unique())
    return [{'label': op, 'value': op} for op in opcoes], None

@callback(
    Output('grafico-barras', 'figure'),
    Output('grafico-boxplot', 'figure'),
    Output('grafico-pizza', 'figure'),
    Input('tax-level-filter', 'value'),
    Input('bacteria-filter', 'value'),
)

def update_graphs(tax_level, selected_bacteria):
    #Cores padrão
    cores = {'TEA': '#FF5733', 'Controle': '#33C1FF'}

    if df.empty:
        vazio = px.bar(title = 'Sem dados')
        return vazio, vazio, vazio

    dff = df.copy()

    #Lógica de filtragem de dados e títulos
    if selected_bacteria:
        dff = dff[dff[tax_level] == selected_bacteria]
        titulo_sulfixo = f"Divisão por grupo: {selected_bacteria}"

        #Para o gráfico em pizza, caso apenas uma bactéria seja filtrada, mostrará a divisão por grupo
        pizza_coluna = 'Group'
        pizza_titulo = f"Divisão por grupo: {selected_bacteria}"
    else:
        #Top 10 bactérias para não sobrecarregar as consultas
        top_bacterias = dff.groupby(tax_level)['Abundance'].sum().nlargest(10).index
        dff = dff[dff[tax_level].isin(top_bacterias)]
        titulo_sulfixo = " (Top 10)"
        pizza_coluna = tax_level
        pizza_titulo = f" Top 10 {tax_level} mais abundantes."


    #Gráfico 1: Barras
    df_grouped = dff.groupby(['Group', tax_level])['Abundance'].mean().reset_index()
    fig_bar = px.bar(
        df_grouped, x = tax_level, y = 'Abundance', color = 'Group', barmode='group',
        title = f"Média{titulo_sulfixo}", color_discrete_map = cores, template = "plotly_white"
    )

    #Gráfico 2: Boxplot
    fig_box = px.box(
        dff, x = 'Group', y = 'Abundance', color = 'Group', points = 'outliers',
        title = f"Dispersão{titulo_sulfixo}", color_discrete_map = cores, template = "plotly_white"
    )
    fig_box.update_layout(yaxis_type = 'log', showlegend = False)

    #Gráfico 3: Pizza
    fig_pie = px.pie(
        dff,
        values = 'Abundance',
        names = pizza_coluna, #<- Altera dinamicamente entre bactéria ou grupo
        title = pizza_titulo,
        hole = 0.4, #<- Transforma o gráfico em rosca, tipo donut
        template = "plotly_white"
    )
    #Se o dashboard estiver mostrando grupos, usa as cores oficiais. Se for bactérias, usa automático.
    if pizza_coluna == 'Group':
        fig_pie.update_traces(marker = dict(colors = [cores[x] for x in dff['Group'].unique()]))

    return fig_bar, fig_box, fig_pie

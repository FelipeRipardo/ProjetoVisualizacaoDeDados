import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

#Registra a página inicial como (path = '/')
dash.register_page(__name__, path = '/', name = 'Início')

layout = dbc.Container([
    #Seção Hero -> Título e Chamada
    dbc.Row([
        dbc.Col([
            html.H1("O papel da microbiota em crianças com diagnóstico de TEA (Transtorno do Espectro Autista)", className = 'display-4 fw-bold text-primary'),
            html.P(
                "Uma análise exploratória de dados sobre a conexão intestino-cérebro "
                "em crianças com Transtorno do Espectro Autista(TEA).",
                className = 'lead text-muted'
            ),
            html.Hr(className = 'my-4'),
            html.P(
                "Este projeto utiliza dados reais de sequenciamento genético (16S rRNA) para identificar "
                "padrões de diversidade bacteriana e potenciais biomarcadores."
            ),
            dbc.Button("Acessar Dashboard de Dados", color = 'primary', href = '/dashboard', size = 'lg', className = 'mt-3 shadow')
        ], width = 12, className = 'text-center py-5')
    ]),

    #Seção de contexto -> Storytelling
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('🧬 O Problema', className = 'card-title'),
                    html.P("O diagnóstico de TEA é clínico e subjetivo. Estudos recentes indicam "
                           "que a disbiose intestinal (desequilíbrio bacteriano) é frequente "
                           "e pode ser um marcador biológico.")
                ])
            ], className = 'h-100 shadow-sm border-0')
        ], width = 4),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📊 Os Dados", className = 'card-title'),
                    html.P("Utilizamos o dataset GSE113690 (Kaggle/NCBI), contendo a abundância de filos e "
                           "gêneros bacterianos de crianças neurotípicas (Controle) e com TEA.")
                ])
            ], className = 'h-100 shadow-sm border-0')
        ], width = 4),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("🎯 O Objetivo", className = 'card-title'),
                    html.P("Aplicar técnicas de Visualização de Dados para validar se existe diferença "
                           "estatística observável na composição da microbiota entre os grupos.")
                ])
            ], className = 'h-100 shadow-sm border-0')
        ], width = 4),
    ], className = 'mt-4 mb-5')
])
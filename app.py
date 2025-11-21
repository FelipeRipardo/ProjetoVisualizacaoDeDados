import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

#Inicialização do app com multipáginas e bootstrap.
app = Dash(__name__, use_pages = True, external_stylesheets = [dbc.themes.FLATLY])
server = app.server

#Barra de navegação do dashboard
navbar = dbc.NavbarSimple(
    children = [
        dbc.NavItem(dbc.NavLink("Início", href ="/")),
        dbc.NavItem(dbc.NavLink("Dashboard de Análise", href = "/dashboard"))
    ],
    brand = "Microbiota & TEA",
    brand_href = "/",
    color = "primary",
    dark = True
)

#Layout principal da aplicação
app.layout = html.Div([
    navbar,
    #Conteiner onde as páginas(pages: dashboard, home) serão carregadas
    dbc.Container(
        dash.page_container,
        fluid = True,
        className = "p-4" #<- 4 unidades de padding
    )
])

if __name__ == '__main__':
    app.run(debug = True)
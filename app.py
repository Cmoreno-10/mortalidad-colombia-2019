from dash import Dash, html
from components.mapa import build_mapa_component
from components.barras_violencia import build_barras_violencia_component
from components.lineas import build_lineas_component
from components.circular import build_circular_component
from components.barras_apiladas import build_barras_apiladas_component
from components.tabla import build_tabla_component
from components.histograma import build_histograma_component
from utils.data_loader import get_mortalidad_data


app = Dash(
    __name__,
    title="Mortalidad Colombia 2019",
    suppress_callback_exceptions=True,
)

server = app.server


def build_summary_cards() -> html.Div:
    """
    Construye tarjetas generales con indicadores básicos.
    """
    df = get_mortalidad_data()

    total_muertes = len(df)
    total_departamentos = df["DEPARTAMENTO"].nunique()
    total_municipios = df["MUNICIPIO"].nunique()
    total_causas = df["CODIGO_CAUSA"].nunique()

    return html.Div(
        className="summary-grid",
        children=[
            html.Div(
                className="summary-card",
                children=[
                    html.H3(f"{total_muertes:,}".replace(",", ".")),
                    html.P("Total de muertes registradas"),
                ],
            ),
            html.Div(
                className="summary-card",
                children=[
                    html.H3(total_departamentos),
                    html.P("Departamentos"),
                ],
            ),
            html.Div(
                className="summary-card",
                children=[
                    html.H3(total_municipios),
                    html.P("Municipios"),
                ],
            ),
            html.Div(
                className="summary-card",
                children=[
                    html.H3(total_causas),
                    html.P("Causas CIE-10"),
                ],
            ),
        ],
    )


def build_placeholder(title: str, description: str) -> html.Div:
    """
    Crea una tarjeta temporal donde luego ubicaremos cada gráfico.
    """
    return html.Div(
        className="chart-card placeholder-card",
        children=[
            html.H2(title),
            html.P(description),
        ],
    )


app.layout = html.Div(
    className="app-container",
    children=[
        html.Header(
            className="hero",
            children=[
                html.H1("Dashboard de Mortalidad en Colombia — 2019"),
                html.P(
                    "Aplicación interactiva para analizar registros de mortalidad "
                    "por territorio, causa, sexo, mes y grupos de edad."
                ),
            ],
        ),

        build_summary_cards(),

        html.Main(
            className="dashboard-grid",
            children=[
                build_mapa_component(),
                
		build_lineas_component(),
                
		build_barras_violencia_component(),

                build_circular_component(),

                build_tabla_component(),

                build_barras_apiladas_component(),

                build_histograma_component(),
            ],
        ),
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)

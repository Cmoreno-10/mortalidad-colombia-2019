import plotly.express as px
from dash import dcc, html

from utils.data_loader import get_mortalidad_data


def build_circular_component() -> html.Div:
    """
    Construye un gráfico donut con los 10 municipios
    con menor número de muertes registradas.
    """
    df = get_mortalidad_data().copy()

    municipios_df = (
        df.groupby("MUNICIPIO")
        .size()
        .reset_index(name="TOTAL_MUERTES")
        .sort_values("TOTAL_MUERTES", ascending=True)
        .head(10)
    )

    fig = px.pie(
        municipios_df,
        names="MUNICIPIO",
        values="TOTAL_MUERTES",
        hole=0.45,
    )

    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Total muertes: %{value}<br>Porcentaje: %{percent}<extra></extra>",
    )

    fig.update_layout(
        height=420,
        margin={"r": 20, "t": 20, "l": 20, "b": 20},
        showlegend=True,
        legend_title_text="Municipio",
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
    )

    return html.Div(
        className="chart-card",
        children=[
            html.H2("10 municipios con menor mortalidad"),
            html.P(
                "Distribución porcentual de los municipios con menor número "
                "de registros de mortalidad total."
            ),
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False},
                responsive=True,
            ),
        ],
    )

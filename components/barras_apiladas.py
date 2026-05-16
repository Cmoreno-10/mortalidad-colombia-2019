import plotly.express as px
from dash import dcc, html

from utils.data_loader import get_mortalidad_data


def build_barras_apiladas_component() -> html.Div:
    """
    Construye un gráfico de barras apiladas por departamento y sexo.
    """
    df = get_mortalidad_data().copy()

    grouped_df = (
        df.groupby(["DEPARTAMENTO", "SEXO_NORMALIZADO"])
        .size()
        .reset_index(name="TOTAL_MUERTES")
        .sort_values("TOTAL_MUERTES", ascending=False)
    )

    fig = px.bar(
        grouped_df,
        x="DEPARTAMENTO",
        y="TOTAL_MUERTES",
        color="SEXO_NORMALIZADO",
        barmode="stack",
        title=None,
        labels={
            "DEPARTAMENTO": "Departamento",
            "TOTAL_MUERTES": "Total de muertes",
            "SEXO_NORMALIZADO": "Sexo",
        },
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Total muertes: %{y}<br>"
            "Sexo: %{legendgroup}<extra></extra>"
        )
    )

    fig.update_layout(
        height=520,
        margin={"r": 20, "t": 20, "l": 20, "b": 120},
        xaxis_tickangle=-45,
        xaxis_title="Departamento",
        yaxis_title="Total de muertes",
        legend_title_text="Sexo",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
    )

    fig.update_yaxes(gridcolor="#e5e7eb")

    return html.Div(
        className="chart-card",
        children=[
            html.H2("Muertes por sexo y departamento"),
            html.P(
                "Comparación del total de defunciones por departamento, "
                "segmentadas por sexo."
            ),
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False},
                responsive=True,
            ),
        ],
    )

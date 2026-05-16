import pandas as pd
import plotly.express as px
from dash import dcc, html

from utils.data_loader import get_mortalidad_data


MONTH_NAMES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}


def build_lineas_component() -> html.Div:
    """
    Construye el gráfico de líneas con el total de muertes por mes.
    """
    df = get_mortalidad_data().copy()

    df["MES"] = pd.to_numeric(df["MES"], errors="coerce")

    monthly_df = (
        df.dropna(subset=["MES"])
        .groupby("MES")
        .size()
        .reset_index(name="TOTAL_MUERTES")
        .sort_values("MES")
    )

    monthly_df["MES_NOMBRE"] = monthly_df["MES"].astype(int).map(MONTH_NAMES)

    fig = px.line(
        monthly_df,
        x="MES_NOMBRE",
        y="TOTAL_MUERTES",
        markers=True,
        text="TOTAL_MUERTES",
        title=None,
    )

    fig.update_traces(
        line=dict(width=4),
        marker=dict(size=9),
        textposition="top center",
        hovertemplate="<b>%{x}</b><br>Total muertes: %{y}<extra></extra>",
    )

    fig.update_layout(
        height=420,
        margin={"r": 20, "t": 20, "l": 20, "b": 20},
        xaxis_title="Mes",
        yaxis_title="Total de muertes",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
    )

    fig.update_yaxes(
        gridcolor="#e5e7eb",
    )

    return html.Div(
        className="chart-card",
        children=[
            html.H2("Muertes por mes — 2019"),
            html.P(
                "Evolución mensual del total de defunciones registradas "
                "durante el año 2019."
            ),
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False},
                responsive=True,
            ),
        ],
    )

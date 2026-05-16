import plotly.express as px
from dash import dcc, html

from utils.data_loader import get_mortalidad_data


def build_barras_violencia_component() -> html.Div:
    """
    Construye el gráfico de barras con el Top 5 de municipios
    con más muertes asociadas al código CIE-10 X95.
    """
    df = get_mortalidad_data().copy()

    df["CODIGO_CAUSA"] = df["CODIGO_CAUSA"].astype(str).str.strip().str.upper()

    violencia_df = df[
    df["CODIGO_CAUSA"].str.startswith("X95", na=False)
    ]

    top_municipios_df = (
        violencia_df.groupby("MUNICIPIO")
        .size()
        .reset_index(name="TOTAL_HOMICIDIOS")
        .sort_values("TOTAL_HOMICIDIOS", ascending=False)
        .head(5)
    )

    fig = px.bar(
        top_municipios_df,
        x="TOTAL_HOMICIDIOS",
        y="MUNICIPIO",
        orientation="h",
        text="TOTAL_HOMICIDIOS",
        title=None,
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Casos X95: %{x}<extra></extra>",
    )

    fig.update_layout(
        height=420,
        margin={"r": 40, "t": 20, "l": 20, "b": 20},
        xaxis_title="Total de homicidios X95",
        yaxis_title="Municipio",
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
    )

    fig.update_xaxes(gridcolor="#e5e7eb")

    return html.Div(
        className="chart-card",
        children=[
            html.H2("Top 5 ciudades más violentas — CIE-10 X95"),
            html.P(
                "Municipios con mayor número de registros asociados a agresión "
                "con disparo de arma de fuego."
            ),
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False},
                responsive=True,
            ),
        ],
    )

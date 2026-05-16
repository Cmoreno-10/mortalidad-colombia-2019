import plotly.express as px
from dash import dcc, html

from utils.data_loader import get_mortalidad_data


AGE_ORDER = [
    "Mortalidad neonatal",
    "Mortalidad infantil",
    "Primera infancia",
    "Niñez",
    "Adolescencia",
    "Juventud",
    "Adultez temprana",
    "Adultez intermedia",
    "Vejez",
    "Longevidad/Centenarios",
    "Edad desconocida",
]


def build_histograma_component() -> html.Div:
    """
    Construye un gráfico de barras tipo histograma categórico
    con la distribución de muertes por grupo de edad.
    """
    df = get_mortalidad_data().copy()

    edad_df = (
        df.groupby("CATEGORIA_EDAD")
        .size()
        .reset_index(name="TOTAL_MUERTES")
    )

    edad_df["CATEGORIA_EDAD"] = edad_df["CATEGORIA_EDAD"].astype(str)

    fig = px.bar(
        edad_df,
        x="CATEGORIA_EDAD",
        y="TOTAL_MUERTES",
        text="TOTAL_MUERTES",
        category_orders={"CATEGORIA_EDAD": AGE_ORDER},
        labels={
            "CATEGORIA_EDAD": "Grupo de edad",
            "TOTAL_MUERTES": "Total de muertes",
        },
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Total muertes: %{y}<extra></extra>",
    )

    fig.update_layout(
        height=520,
        margin={"r": 20, "t": 20, "l": 20, "b": 120},
        xaxis_tickangle=-35,
        xaxis_title="Grupo de edad",
        yaxis_title="Total de muertes",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
    )

    fig.update_yaxes(gridcolor="#e5e7eb")

    return html.Div(
        className="chart-card",
        children=[
            html.H2("Distribución de muertes por grupos de edad"),
            html.P(
                "Clasificación de la mortalidad según grupos etarios derivados "
                "de códigos DANE."
            ),
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False},
                responsive=True,
            ),
        ],
    )

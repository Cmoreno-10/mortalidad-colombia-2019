import json
from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import dcc, html

from utils.data_loader import get_mortalidad_data


BASE_DIR = Path(__file__).resolve().parent.parent
GEOJSON_FILE = BASE_DIR / "data" / "colombia_departamentos.geojson"


def normalize_department_name(name: str) -> str:
    """
    Normaliza nombres de departamentos para mejorar coincidencias
    entre GeoJSON y DataFrame.
    """
    if pd.isna(name):
        return ""

    return (
        str(name)
        .strip()
        .upper()
        .replace("Á", "A")
        .replace("É", "E")
        .replace("Í", "I")
        .replace("Ó", "O")
        .replace("Ú", "U")
    )


def build_mapa_component() -> html.Div:
    """
    Construye el mapa coroplético de mortalidad por departamento.
    """

    # =========================
    # Cargar datos
    # =========================
    df = get_mortalidad_data()

    # =========================
    # Agrupar por departamento
    # =========================
    departamentos_df = (
        df.groupby("DEPARTAMENTO")
        .size()
        .reset_index(name="TOTAL_MUERTES")
    )

    # =========================
    # Normalizar nombres
    # =========================
    departamentos_df["DEPARTAMENTO_NORMALIZADO"] = (
        departamentos_df["DEPARTAMENTO"]
        .apply(normalize_department_name)
    )

    # =========================
    # Cargar GeoJSON
    # =========================
    with open(GEOJSON_FILE, "r", encoding="utf-8") as file:
        geojson_data = json.load(file)

    # =========================
    # Normalizar nombres GeoJSON
    # =========================
    for feature in geojson_data["features"]:
        feature["properties"]["NOMBRE_NORMALIZADO"] = normalize_department_name(
            feature["properties"]["NOMBRE_DPT"]
        )

    # =========================
    # Construir mapa
    # =========================
    fig = px.choropleth(
    departamentos_df,
    geojson=geojson_data,
    locations="DEPARTAMENTO_NORMALIZADO",
    featureidkey="properties.NOMBRE_NORMALIZADO",
    color="TOTAL_MUERTES",
    hover_name="DEPARTAMENTO",
    hover_data={
        "TOTAL_MUERTES": True,
        "DEPARTAMENTO_NORMALIZADO": False,
    },
    color_continuous_scale="YlOrRd",
    projection="mercator",
    )

    fig.update_geos(
    fitbounds="locations",
    visible=False,
    )

    fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=600,
    coloraxis_colorbar={"title": "Muertes"},
    )

    # =========================
    # Diseño del gráfico
    # =========================
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=600,
        coloraxis_colorbar={
            "title": "Muertes"
        },
    )

    return html.Div(
        className="chart-card",
        children=[
            html.H2("Mapa de Mortalidad por Departamento"),
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False},
                responsive=True,
            ),
        ],
    )

from dash import dash_table, html

from utils.data_loader import get_mortalidad_data


def build_tabla_component() -> html.Div:
    """
    Construye una tabla interactiva con el Top 10 de causas de muerte.
    """
    df = get_mortalidad_data().copy()

    top_causas_df = (
        df.groupby(["CODIGO_CAUSA", "NOMBRE_CAUSA"])
        .size()
        .reset_index(name="TOTAL_CASOS")
        .sort_values("TOTAL_CASOS", ascending=False)
        .head(10)
    )

    return html.Div(
        className="chart-card",
        children=[
            html.H2("Top 10 causas de muerte en Colombia"),
            html.P(
                "Ranking de las causas de muerte más frecuentes según código CIE-10."
            ),
            dash_table.DataTable(
                data=top_causas_df.to_dict("records"),
                columns=[
                    {"name": "Código CIE-10", "id": "CODIGO_CAUSA"},
                    {"name": "Nombre de la causa", "id": "NOMBRE_CAUSA"},
                    {"name": "Total de casos", "id": "TOTAL_CASOS"},
                ],
                page_size=10,
                sort_action="native",
                filter_action="native",
                style_table={
                    "overflowX": "auto",
                    "overflowY": "auto",
                    "maxHeight": "420px",
                },
                style_cell={
                    "fontFamily": "Arial",
                    "fontSize": "14px",
                    "padding": "12px",
                    "textAlign": "left",
                    "whiteSpace": "normal",
                    "height": "auto",
                    "minWidth": "120px",
                    "maxWidth": "420px",
                },
                style_header={
                    "backgroundColor": "#102a43",
                    "color": "white",
                    "fontWeight": "bold",
                    "border": "1px solid #d1d5db",
                },
                style_data={
                    "backgroundColor": "white",
                    "color": "#1f2937",
                    "border": "1px solid #e5e7eb",
                },
                style_data_conditional=[
                    {
                        "if": {"row_index": "odd"},
                        "backgroundColor": "#f8fafc",
                    },
                    {
                        "if": {"column_id": "TOTAL_CASOS"},
                        "fontWeight": "bold",
                        "color": "#102a43",
                    },
                ],
            ),
        ],
    )

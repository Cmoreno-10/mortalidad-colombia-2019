from functools import lru_cache
from pathlib import Path
from typing import Dict

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

MORTALIDAD_FILE = DATA_DIR / "datos_mortalidad.xlsx"
CAUSAS_FILE = DATA_DIR / "codigos_causas_muerte.xlsx"
DIVIPOLA_FILE = DATA_DIR / "division_politico_administrativa.xlsx"


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia los nombres de columnas para trabajar de forma más segura.
    Convierte nombres a mayúsculas, elimina espacios y reemplaza espacios por guiones bajos.
    """
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.upper()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def read_excel_file(file_path: Path) -> pd.DataFrame:
    """
    Lee un archivo Excel y maneja errores comunes.
    """
    try:
        return pd.read_excel(file_path, engine="openpyxl")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}") from exc
    except Exception as exc:
        raise RuntimeError(f"Error leyendo el archivo {file_path.name}: {exc}") from exc


def normalize_code_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Convierte columnas de códigos a texto para evitar errores en cruces.
    Ejemplo: 05 no debe convertirse en 5.
    """
    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = df[column].astype(str).str.strip()

    return df


def build_age_group_category(code: object) -> str:
    """
    Convierte el código DANE de GRUPO_EDAD1 en una categoría entendible.
    """
    try:
        age_code = int(code)
    except (ValueError, TypeError):
        return "Edad desconocida"

    if 0 <= age_code <= 4:
        return "Mortalidad neonatal"
    if 5 <= age_code <= 6:
        return "Mortalidad infantil"
    if 7 <= age_code <= 8:
        return "Primera infancia"
    if 9 <= age_code <= 10:
        return "Niñez"
    if age_code == 11:
        return "Adolescencia"
    if 12 <= age_code <= 13:
        return "Juventud"
    if 14 <= age_code <= 16:
        return "Adultez temprana"
    if 17 <= age_code <= 19:
        return "Adultez intermedia"
    if 20 <= age_code <= 24:
        return "Vejez"
    if 25 <= age_code <= 28:
        return "Longevidad/Centenarios"
    if age_code == 29:
        return "Edad desconocida"

    return "Edad desconocida"


def normalize_sex(value: object) -> str:
    """
    Normaliza la variable sexo.
    Ajustaremos esta función si tus datos usan códigos diferentes.
    """
    value_str = str(value).strip().upper()

    mapping = {
        "1": "Masculino",
        "M": "Masculino",
        "MASCULINO": "Masculino",
        "HOMBRE": "Masculino",
        "2": "Femenino",
        "F": "Femenino",
        "FEMENINO": "Femenino",
        "MUJER": "Femenino",
        "3": "Indeterminado",
        "I": "Indeterminado",
        "INDETERMINADO": "Indeterminado",
        "SIN INFORMACION": "Indeterminado",
        "SIN INFORMACIÓN": "Indeterminado",
        "NAN": "Indeterminado",
    }

    return mapping.get(value_str, "Indeterminado")


@lru_cache(maxsize=1)
def load_data() -> Dict[str, pd.DataFrame]:
    """
    Carga, limpia y prepara los datos principales del proyecto.

    Retorna un diccionario con:
    - mortalidad: base completa enriquecida
    - causas: tabla de causas CIE-10
    - divipola: tabla territorial DANE
    """
    mortalidad = clean_column_names(read_excel_file(MORTALIDAD_FILE))

    causas = clean_column_names(
        pd.read_excel(
            CAUSAS_FILE,
            engine="openpyxl",
            header=8
        )
    )

    divipola = clean_column_names(read_excel_file(DIVIPOLA_FILE))

    causas = clean_column_names(
    pd.read_excel(
        CAUSAS_FILE,
        engine="openpyxl",
        header=8
    )
)

    mortalidad = normalize_code_columns(
        mortalidad,
        ["COD_DPTO", "COD_MUNIC", "COD_MUNICIPIO", "COD_DANE", "CAUSA_DEF", "GRUPO_EDAD1"],
    )

    causas = normalize_code_columns(
        causas,
        ["CODIGO", "COD_CIE10", "CAUSA_DEF"],
    )

    divipola = normalize_code_columns(
      divipola,
        ["COD_DPTO", "COD_MUNIC", "COD_MUNICIPIO", "COD_DANE"],
    )

    # Normalizar posible columna de causa de muerte
    if "CAUSA_DEF" in mortalidad.columns:
    	mortalidad["CODIGO_CAUSA"] = mortalidad["CAUSA_DEF"]
    elif "COD_CIE10" in mortalidad.columns:
    	mortalidad["CODIGO_CAUSA"] = mortalidad["COD_CIE10"]
    elif "COD_MUERTE" in mortalidad.columns:
    	mortalidad["CODIGO_CAUSA"] = mortalidad["COD_MUERTE"]
    else:
    	raise KeyError("No se encontró columna de causa de muerte en mortalidad.")

    # Normalizar tabla de causas
    if "CODIGO" in causas.columns:
    	causas["CODIGO_CAUSA"] = causas["CODIGO"]

    elif "COD_CIE10" in causas.columns:
    	causas["CODIGO_CAUSA"] = causas["COD_CIE10"]

    elif "CAUSA_DEF" in causas.columns:
    	causas["CODIGO_CAUSA"] = causas["CAUSA_DEF"]

    elif "CÓDIGO_DE_LA_CIE_10_TRES_CARACTERES" in causas.columns:
    	causas["CODIGO_CAUSA"] = causas["CÓDIGO_DE_LA_CIE_10_TRES_CARACTERES"]

    elif "CODIGO_DE_LA_CIE_10_TRES_CARACTERES" in causas.columns:
    	causas["CODIGO_CAUSA"] = causas["CODIGO_DE_LA_CIE_10_TRES_CARACTERES"]

    else:
    	raise KeyError("No se encontró columna de código CIE-10 en causas.")

    # Buscar columna de nombre de causa
    possible_cause_names = [
    "NOMBRE_CAUSA",
    "DESCRIPCION",
    "DESCRIPCIÓN",
    "CAUSA",
    "NOMBRE",
    "DESCRIPCIÓN_DE_CÓDIGOS_MORTALIDAD_A_TRES_CARACTERES",
    "DESCRIPCION_DE_CODIGOS_MORTALIDAD_A_TRES_CARACTERES",
	]
    cause_name_column = next((col for col in possible_cause_names if col in causas.columns), None)

    if cause_name_column is None:
        causas["NOMBRE_CAUSA"] = "Sin descripción"
    else:
        causas["NOMBRE_CAUSA"] = causas[cause_name_column]

    

        # =========================
    # Normalizar códigos CIE-10 a 3 caracteres
    # =========================
         # =========================
    # Normalizar tabla de causas CIE-10
    # =========================
    causas["CODIGO_CAUSA"] = (
        causas["CODIGO_CAUSA"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    causas["CODIGO_CAUSA_3"] = causas["CODIGO_CAUSA"].str[:3]

    mortalidad["CODIGO_CAUSA"] = (
        mortalidad["CODIGO_CAUSA"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    mortalidad["CODIGO_CAUSA_3"] = mortalidad["CODIGO_CAUSA"].str[:3]
        # =========================
    # Detectar descripción CIE-10
    # =========================
        # =========================
         # =========================
    # Detectar descripción CIE-10
    # =========================
    if "DESCRIPCIÓN__DE_CÓDIGOS_MORTALIDAD_A_TRES_CARACTERES" in causas.columns:
        causas["NOMBRE_CAUSA"] = causas[
            "DESCRIPCIÓN__DE_CÓDIGOS_MORTALIDAD_A_TRES_CARACTERES"
        ]

    elif "DESCRIPCION__DE_CODIGOS_MORTALIDAD_A_TRES_CARACTERES" in causas.columns:
        causas["NOMBRE_CAUSA"] = causas[
            "DESCRIPCION__DE_CODIGOS_MORTALIDAD_A_TRES_CARACTERES"
        ]

    elif "DESCRIPCIÓN__DE_CÓDIGOS_MORTALIDAD_A_CUATRO_CARACTERES" in causas.columns:
        causas["NOMBRE_CAUSA"] = causas[
            "DESCRIPCIÓN__DE_CÓDIGOS_MORTALIDAD_A_CUATRO_CARACTERES"
        ]

    elif "DESCRIPCION__DE_CODIGOS_MORTALIDAD_A_CUATRO_CARACTERES" in causas.columns:
        causas["NOMBRE_CAUSA"] = causas[
            "DESCRIPCION__DE_CODIGOS_MORTALIDAD_A_CUATRO_CARACTERES"
        ]

    else:
        causas["NOMBRE_CAUSA"] = "Sin descripción"


    # Eliminar filas vacías o inválidas en causas
    causas_limpias = causas[
        causas["CODIGO_CAUSA_3"].notna()
        & causas["NOMBRE_CAUSA"].notna()
        & (causas["CODIGO_CAUSA_3"] != "NAN")
    ][["CODIGO_CAUSA_3", "NOMBRE_CAUSA"]].drop_duplicates("CODIGO_CAUSA_3")

    # Cruce por código CIE-10 de 3 caracteres
    mortalidad = mortalidad.merge(
        causas_limpias,
        on="CODIGO_CAUSA_3",
        how="left",
    )

    if "NOMBRE_CAUSA" not in mortalidad.columns:
        print("Columnas disponibles después del merge:")
        print(mortalidad.columns.tolist())
        mortalidad["NOMBRE_CAUSA"] = "Causa no identificada"
    else:
        mortalidad["NOMBRE_CAUSA"] = mortalidad["NOMBRE_CAUSA"].fillna(
            "Causa no identificada"
        )    
  # =========================
    # Cruce usando categoría CIE-10 de 3 caracteres
    # =========================
    if "NOMBRE_CAUSA" not in mortalidad.columns:
        print("Columnas disponibles después del merge:")
        print(mortalidad.columns.tolist())
        mortalidad["NOMBRE_CAUSA"] = "Causa no identificada"
    else:
        mortalidad["NOMBRE_CAUSA"] = mortalidad["NOMBRE_CAUSA"].fillna(
            "Causa no identificada"
        )

    # Normalizar columna de departamento
    if "NOMBRE_DPTO" in divipola.columns:
        divipola["DEPARTAMENTO"] = divipola["NOMBRE_DPTO"]
    elif "DEPARTAMENTO" not in divipola.columns:
        divipola["DEPARTAMENTO"] = "Sin departamento"

    # Normalizar columna de municipio
    if "NOMBRE_MUNICIPIO" in divipola.columns:
        divipola["MUNICIPIO"] = divipola["NOMBRE_MUNICIPIO"]
    elif "NOM_MUNICIPIO" in divipola.columns:
        divipola["MUNICIPIO"] = divipola["NOM_MUNICIPIO"]
    elif "MUNICIPIO" not in divipola.columns:
        divipola["MUNICIPIO"] = "Sin municipio"

    # Cruce territorial flexible
    territorial_keys = []

    if "COD_DANE" in mortalidad.columns and "COD_DANE" in divipola.columns:
        territorial_keys = ["COD_DANE"]
    elif "COD_MUNICIPIO" in mortalidad.columns and "COD_MUNICIPIO" in divipola.columns:
        territorial_keys = ["COD_MUNICIPIO"]
    elif "COD_MUNIC" in mortalidad.columns and "COD_MUNIC" in divipola.columns:
        territorial_keys = ["COD_MUNIC"]
    elif "COD_DPTO" in mortalidad.columns and "COD_DPTO" in divipola.columns:
        territorial_keys = ["COD_DPTO"]

    if territorial_keys:
        mortalidad = mortalidad.merge(
            divipola[territorial_keys + ["DEPARTAMENTO", "MUNICIPIO"]].drop_duplicates(),
            on=territorial_keys,
            how="left",
        )
    else:
        mortalidad["DEPARTAMENTO"] = "Sin departamento"
        mortalidad["MUNICIPIO"] = "Sin municipio"

    mortalidad["DEPARTAMENTO"] = mortalidad["DEPARTAMENTO"].fillna("Sin departamento")
    mortalidad["MUNICIPIO"] = mortalidad["MUNICIPIO"].fillna("Sin municipio")

    # Crear variable mes
    if "MES" in mortalidad.columns:
        mortalidad["MES"] = pd.to_numeric(mortalidad["MES"], errors="coerce")
    elif "MES_DEF" in mortalidad.columns:
        mortalidad["MES"] = pd.to_numeric(mortalidad["MES_DEF"], errors="coerce")
    else:
        mortalidad["MES"] = None

    # Crear variable sexo normalizada
    if "SEXO" in mortalidad.columns:
        mortalidad["SEXO_NORMALIZADO"] = mortalidad["SEXO"].apply(normalize_sex)
    else:
        mortalidad["SEXO_NORMALIZADO"] = "Indeterminado"

    # Crear grupo de edad interpretado
    if "GRUPO_EDAD1" in mortalidad.columns:
        mortalidad["CATEGORIA_EDAD"] = mortalidad["GRUPO_EDAD1"].apply(build_age_group_category)
    else:
        mortalidad["CATEGORIA_EDAD"] = "Edad desconocida"

    return {
        "mortalidad": mortalidad,
        "causas": causas,
        "divipola": divipola,
      }


def get_mortalidad_data() -> pd.DataFrame:
    """
    Retorna únicamente la base de mortalidad enriquecida.
    """
    return load_data()["mortalidad"]


def get_causas_data() -> pd.DataFrame:
    """
    Retorna la tabla de causas.
    """
    return load_data()["causas"]


def get_divipola_data() -> pd.DataFrame:
    """
    Retorna la tabla territorial.
    """
    return load_data()["divipola"]

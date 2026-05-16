# Dashboard de Mortalidad en Colombia — 2019

Aplicación web interactiva desarrollada con Python, Dash y Plotly para el análisis de registros de mortalidad en Colombia durante el año 2019.

El proyecto integra visualizaciones epidemiológicas, análisis territorial y procesamiento de datos provenientes de archivos oficiales en formato Excel.

---

#  Objetivo del proyecto

Analizar el comportamiento de la mortalidad en Colombia mediante herramientas de visualización interactiva que permitan:

- Identificar patrones territoriales.
- Analizar tendencias temporales.
- Explorar causas de muerte según clasificación CIE-10.
- Comparar distribución por sexo y grupos de edad.
- Visualizar eventos asociados a violencia por arma de fuego.

---

# rquitectura del sistema

```text
Archivos Excel
      ↓
Carga y limpieza de datos (Pandas)
      ↓
Transformación y enriquecimiento
      ↓
Componentes visuales Dash + Plotly
      ↓
Dashboard web interactivo
      ↓
Despliegue en Render
```

---

# Estructura del proyecto

```text
mortalidad-colombia-2019/
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── README.md
├── assets/
│   └── style.css
├── data/
│   ├── datos_mortalidad.xlsx
│   ├── codigos_causas_muerte.xlsx
│   ├── division_politico_administrativa.xlsx
│   └── colombia_departamentos.geojson
├── components/
│   ├── mapa.py
│   ├── lineas.py
│   ├── barras_violencia.py
│   ├── circular.py
│   ├── tabla.py
│   ├── barras_apiladas.py
│   └── histograma.py
└── utils/
    ├── data_loader.py
    └── helpers.py
```

---

# ecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.11 | Lenguaje principal |
| Dash | Framework web interactivo |
| Plotly | Visualizaciones |
| Pandas | Procesamiento de datos |
| NumPy | Operaciones numéricas |
| OpenPyXL | Lectura de archivos Excel |
| Gunicorn | Servidor WSGI |
| Render | Despliegue cloud |

---

# Requisitos

Instalar:

- Python 3.10+
- pip
- virtualenv

---

#Instalación local

## 1. Clonar repositorio

```bash
git clone https://github.com/TU_USUARIO/mortalidad-colombia-2019.git
```

## 2. Entrar al proyecto

```bash
cd mortalidad-colombia-2019
```

## 3. Crear entorno virtual

```bash
python -m venv venv
```

## 4. Activar entorno virtual

### Linux / WSL

```bash
source venv/bin/activate
```

### Windows

```powershell
.\venv\Scripts\Activate.ps1
```

## 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

#  Ejecución local

```bash
python app.py
```

Abrir en navegador:

```text
http://localhost:8050
```

---

# Ejecución con Gunicorn

```bash
gunicorn app:server
```

Abrir:

```text
http://localhost:8000
```

---

# Despliegue en Render

## 1. Subir proyecto a GitHub

Crear repositorio y subir el proyecto.

## 2. Crear cuenta en Render

https://render.com

## 3. Crear nuevo Web Service

Seleccionar:

- Runtime: Python
- Build Command:

```bash
pip install -r requirements.txt
```

- Start Command:

```bash
gunicorn app:server
```

## 4. Deploy

Render generará automáticamente una URL pública.

---

#  Visualizaciones implementadas

## 1. Mapa coroplético

- Total de muertes por departamento.
- GeoJSON de Colombia.
- Hover interactivo.

## 2. Gráfico de líneas

- Evolución mensual de mortalidad.

## 3. Barras — Top ciudades violentas

- Basado en código CIE-10 X95.

## 4. Gráfico donut

- Municipios con menor mortalidad.

## 5. Tabla interactiva

- Top 10 causas de muerte.

## 6. Barras apiladas

- Mortalidad por sexo y departamento.

## 7. Histograma de edades

- Distribución por grupos etarios DANE.

---

#  Fuentes de datos

- Registros de mortalidad Colombia 2019
- Clasificación CIE-10
- División político-administrativa DANE

---

#  Características técnicas

- Arquitectura modular.
- Carga optimizada con caché.
- Diseño responsive.
- Manejo robusto de errores.
- Integración geoespacial con GeoJSON.
- Procesamiento ETL para normalización CIE-10.

---

#  Posibles mejoras futuras

- Filtros dinámicos por año.
- Dashboards comparativos multianuales.
- Integración con bases SQL.
- Exportación PDF/Excel.
- Machine Learning predictivo.
- KPIs epidemiológicos avanzados.

---

#Autor

Proyecto desarrollado con Python, Dash y Plotly para análisis epidemiológico y territorial de mortalidad en Colombia.

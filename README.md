![Streamlit](https://img.shields.io/badge/App-Streamlit-red?logo=streamlit)
[Ver app en vivo ↗](https://proyecto-clima-energia-sd8fjbztidffp2vpv2qhk7.streamlit.app/)

# Análisis Global de Clima y Energía 2020–2024

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-purple?logo=plotly)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Completo-green)

> Proyecto final integrador — Talento Tech · Análisis de Datos · 2025

---

## Descripción

Análisis exploratorio completo de un dataset global de clima y energía con registros diarios de **20 países** durante **5 años (2020–2024)**. El proyecto aplica el ciclo completo de análisis de datos: exploración, estadística descriptiva, visualización interactiva, correlaciones, regresión lineal y base de datos SQL.

---

## Estructura del repositorio

    proyecto_clima_energia/
    ├── data/                         # Dataset original y archivos procesados
    ├── notebooks/                    # Análisis en Jupyter Notebook
    │   ├── 01_exploracion_limpieza.ipynb
    │   ├── 02_estadistica_descriptiva.ipynb
    │   ├── 03_dashboard_visualizaciones.ipynb
    │   ├── 04_correlaciones_regresion.ipynb
    │   └── 06_analisis_final_completo.ipynb
    ├── sql/                          # Schema, queries y script de carga
    ├── landing_page/                 # Página web del proyecto
    ├── streamlit_app/                # Prototipo interactivo
    ├── docs/                         # Documento PDF y presentación PPTX
    └── README.md

---

## Dataset

| Característica | Valor |
|---|---|
| Registros totales | 36,540 |
| Países | 20 |
| Período | 2020 – 2024 (diario) |
| Variables | 10 |
| Valores nulos | 0 |

**Variables:** avg_temperature · humidity · co2_emission · energy_consumption · renewable_share · urban_population · industrial_activity_index · energy_price

---

## Hallazgos principales

| Dimensión | Hallazgo | Valor |
|---|---|---|
| Temperatura | Asia-Pacifico lidera en calor | Media global: 13.58°C |
| CO2 | Sin tendencia clara a la baja | Media global: 445.82 |
| Renovables | Gran brecha entre países | Rango: 5% – 30.87% |
| Correlación | Solo CO2 vs consumo es significativa | r = 0.1718 |
| Regresión | Modelo explica poca varianza | R2 = 3.06% |
| Dataset | Naturaleza sintética confirmada | Correlaciones cercanas a 0 |

---

## Stack tecnológico

| Herramienta | Uso |
|---|---|
| Python 3.x | Lenguaje principal |
| Pandas / NumPy | Manipulación de datos |
| Plotly / Seaborn | Visualización interactiva y estática |
| Scikit-learn | Regresión lineal y evaluación |
| SciPy / Statsmodels | Estadística inferencial |
| MySQL + Workbench | Base de datos relacional |
| Streamlit | Prototipo interactivo |
| VS Code + Jupyter | Entorno de desarrollo |

---

## Notebooks

| Notebook | Contenido |
|---|---|
| 01_exploracion_limpieza.ipynb | EDA, calidad del dato, boxplots |
| 02_estadistica_descriptiva.ipynb | Estadísticas por país y región |
| 03_dashboard_visualizaciones.ipynb | Mapas, heatmaps, burbujas |
| 04_correlaciones_regresion.ipynb | Pearson, regresión lineal, R2 |
| 06_analisis_final_completo.ipynb | Notebook unificado completo |

---

## Base de datos SQL

Esquema MySQL con **36,540 registros** y **13 queries analíticas** documentadas que responden las preguntas clave del proyecto.

---

## Cómo ejecutar el proyecto

**1. Clona el repositorio**

    git clone https://github.com/Miguel-sierra89/proyecto-clima-energia.git
    cd proyecto-clima-energia

**2. Crea el entorno virtual e instala dependencias**

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

**3. Abre los notebooks en VS Code**

Abre la carpeta del proyecto en VS Code y selecciona el kernel .venv en cada notebook.

**4. Ejecuta el prototipo Streamlit**

    cd streamlit_app
    streamlit run app.py

---

## Nota metodológica

El dataset utilizado es de naturaleza sintética, generado para práctica de análisis de datos. Las técnicas aplicadas son válidas y replicables sobre datos reales. El análisis estadístico riguroso permitió identificar esta característica, lo que demuestra pensamiento crítico en la interpretación de resultados.

---

## Autor

**Miguel Sierra**
Programa: Talento Tech — Análisis de Datos · 2025
GitHub: [@Miguel-sierra89](https://github.com/Miguel-sierra89)

---

*Proyecto final integrador — Talento Tech 2025*

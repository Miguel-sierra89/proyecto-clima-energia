---

## Dataset

| Característica | Valor |
|---|---|
| Registros totales | 36,540 |
| Países | 20 |
| Período | 2020 – 2024 (diario) |
| Variables | 10 |
| Valores nulos | 0 |

**Variables:** `avg_temperature` · `humidity` · `co2_emission` ·
`energy_consumption` · `renewable_share` · `urban_population` ·
`industrial_activity_index` · `energy_price`

---

## Hallazgos principales

| Dimensión | Hallazgo | Valor |
|---|---|---|
| Temperatura | Asia-Pacifico lidera en calor | Media global: 13.58°C |
| CO₂ | Sin tendencia clara a la baja | Media global: 445.82 |
| Renovables | Gran brecha entre países | Rango: 5% – 30.87% |
| Correlación | Solo CO₂ vs consumo es significativa | r = 0.1718 |
| Regresión | Modelo explica poca varianza | R² = 3.06% |
| Dataset | Naturaleza sintética confirmada | Correlaciones ≈ 0 |

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

| # | Notebook | Contenido |
|---|---|---|
| 1 | `01_exploracion_limpieza.ipynb` | EDA, calidad del dato, boxplots |
| 2 | `02_estadistica_descriptiva.ipynb` | Estadísticas por país y región |
| 3 | `03_dashboard_visualizaciones.ipynb` | Mapas, heatmaps, burbujas |
| 4 | `04_correlaciones_regresion.ipynb` | Pearson, regresión lineal, R² |
| 6 | `06_analisis_final_completo.ipynb` | Notebook unificado completo |

---

## Base de datos SQL

Esquema MySQL con **36,540 registros** y **13 queries analíticas** documentadas que responden las preguntas clave del proyecto.

```sql
-- Ejemplo: Top 5 países mejor desempeño ambiental
SELECT pais, region,
    ROUND(AVG(participacion_renovable), 2) AS renovable_promedio,
    ROUND(AVG(emision_co2), 2)             AS co2_promedio,
    ROUND(AVG(participacion_renovable) /
          AVG(emision_co2) * 100, 4)       AS indice_ambiental
FROM registros_clima_energia
GROUP BY pais, region
ORDER BY indice_ambiental DESC
LIMIT 5;
```

---

## Cómo ejecutar el proyecto

### 1. Clona el repositorio
```bash
git clone https://github.com/Miguel-sierra89/proyecto-clima-energia.git
cd proyecto-clima-energia
```

### 2. Crea el entorno virtual e instala dependencias
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Abre los notebooks
```bash
# En VS Code abre la carpeta y selecciona el kernel .venv
# O lanza Jupyter directamente:
jupyter notebook notebooks/
```

### 4. Ejecuta el prototipo Streamlit
```bash
cd streamlit_app
streamlit run app.py
```

---

## Nota metodológica

> El dataset utilizado es de naturaleza sintética, generado para práctica
> de análisis de datos. Las técnicas aplicadas son válidas y replicables
> sobre datos reales. El análisis estadístico riguroso permitió identificar
> esta característica — lo que demuestra pensamiento crítico en la
> interpretación de resultados.

---

## Autor

**Miguel Sierra**  
Programa: Talento Tech — Análisis de Datos · 2025  
GitHub: [@Miguel-sierra89](https://github.com/Miguel-sierra89)

---

*Proyecto final integrador — Talento Tech 2025*
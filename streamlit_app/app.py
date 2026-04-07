import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

# ── Configuración de la página ─────────────────────────
st.set_page_config(
    page_title="Clima y Energía 2020–2024",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilos CSS ────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #F1F9FF; }
    .metric-card {
        background: white; border-radius: 12px;
        padding: 1rem 1.2rem; border-left: 4px solid #0D9488;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .metric-value { font-size: 1.8rem; font-weight: 800; color: #065A82; }
    .metric-label { font-size: 0.82rem; color: #64748B; margin-top: 0.2rem; }
    .insight-box {
        background: #E0F2FE; border-radius: 10px;
        padding: 1rem 1.2rem; margin: 0.5rem 0;
        border-left: 4px solid #065A82;
    }
    .section-title {
        font-size: 1.4rem; font-weight: 700;
        color: #065A82; margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Carga de datos ─────────────────────────────────────
@st.cache_data
def cargar_datos():
    df = pd.read_csv("data/dataset_limpio.csv", parse_dates=["date"])
    df["year"]  = df["date"].dt.year
    df["month"] = df["date"].dt.month
    regiones = {
        "Germany":"Europa","France":"Europa","United Kingdom":"Europa",
        "Italy":"Europa","Spain":"Europa","Sweden":"Europa",
        "Norway":"Europa","Netherlands":"Europa","Poland":"Europa",
        "Turkey":"Europa",
        "United States":"América","Canada":"América",
        "Mexico":"América","Brazil":"América",
        "China":"Asia-Pacífico","India":"Asia-Pacífico",
        "Japan":"Asia-Pacífico","Indonesia":"Asia-Pacífico",
        "Australia":"Asia-Pacífico",
        "South Africa":"África"
    }
    df["region"] = df["country"].map(regiones)
    return df

df = cargar_datos()

# ── Sidebar ────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.shields.io/badge/Talento%20Tech-2025-0D9488?style=for-the-badge")
    st.markdown("## Filtros")

    # Filtro de años
    años_disponibles = sorted(df["year"].unique())
    años_sel = st.slider(
        "Rango de años",
        min_value=int(min(años_disponibles)),
        max_value=int(max(años_disponibles)),
        value=(int(min(años_disponibles)), int(max(años_disponibles)))
    )

    # Filtro de regiones
    regiones_disponibles = sorted(df["region"].unique())
    regiones_sel = st.multiselect(
        "Regiones",
        options=regiones_disponibles,
        default=regiones_disponibles
    )

    # Filtro de países
    paises_disponibles = sorted(
        df[df["region"].isin(regiones_sel)]["country"].unique()
    )
    paises_sel = st.multiselect(
        "Países",
        options=paises_disponibles,
        default=paises_disponibles[:6]
    )

    st.markdown("---")
    st.markdown("**Variable para análisis**")
    variable_sel = st.selectbox(
        "Variable principal",
        options=[
            "avg_temperature", "co2_emission", "energy_consumption",
            "renewable_share", "energy_price", "industrial_activity_index"
        ],
        format_func=lambda x: {
            "avg_temperature":          "🌡️ Temperatura (°C)",
            "co2_emission":             "💨 Emisiones CO₂",
            "energy_consumption":       "⚡ Consumo energético",
            "renewable_share":          "🌱 % Renovable",
            "energy_price":             "💰 Precio energía",
            "industrial_activity_index":"🏭 Actividad industrial"
        }[x]
    )

    st.markdown("---")
    st.markdown("**Miguel Sierra**  \nTalento Tech · 2025")
    st.markdown("[GitHub ↗](https://github.com/Miguel-sierra89/proyecto-clima-energia)")

# ── Filtrar datos ──────────────────────────────────────
df_f = df[
    (df["year"] >= años_sel[0]) &
    (df["year"] <= años_sel[1]) &
    (df["region"].isin(regiones_sel))
]

# ── Header principal ───────────────────────────────────
st.markdown("# 🌍 Análisis Global de Clima y Energía 2020–2024")
st.markdown("Exploración interactiva de patrones climáticos, emisiones de CO₂ y transición energética en 20 países.")
st.markdown("---")

# ── KPIs ───────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Registros", f"{len(df_f):,}", help="Total de registros con filtros aplicados")
with col2:
    st.metric("Países", df_f["country"].nunique())
with col3:
    st.metric("Temp. promedio", f"{df_f['avg_temperature'].mean():.1f}°C")
with col4:
    st.metric("CO₂ promedio", f"{df_f['co2_emission'].mean():.0f}")
with col5:
    st.metric("% Renovable", f"{df_f['renewable_share'].mean():.1f}%")

st.markdown("---")

# ══════════════════════════════════════════════════════
# SECCIÓN 1 — MAPA MUNDIAL
# ══════════════════════════════════════════════════════
st.markdown('<div class="section-title">🗺️ Mapa mundial</div>', unsafe_allow_html=True)

col_mapa1, col_mapa2 = st.columns([3, 1])

with col_mapa2:
    variable_mapa = st.selectbox(
        "Variable del mapa",
        options=["avg_temperature","co2_emission","renewable_share",
                 "energy_consumption","energy_price"],
        format_func=lambda x: {
            "avg_temperature":    "Temperatura",
            "co2_emission":       "CO₂",
            "renewable_share":    "% Renovable",
            "energy_consumption": "Consumo energético",
            "energy_price":       "Precio energía"
        }[x]
    )
    escalas = {
        "avg_temperature":    "RdYlBu_r",
        "co2_emission":       "Reds",
        "renewable_share":    "Greens",
        "energy_consumption": "Blues",
        "energy_price":       "Oranges"
    }

with col_mapa1:
    mapa_data = df_f.groupby("country")[variable_mapa].mean().reset_index()
    fig_mapa = px.choropleth(
        mapa_data,
        locations="country",
        locationmode="country names",
        color=variable_mapa,
        color_continuous_scale=escalas[variable_mapa],
        height=420
    )
    fig_mapa.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        geo=dict(showframe=False, showcoastlines=True)
    )
    st.plotly_chart(fig_mapa, use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════════════
# SECCIÓN 2 — EVOLUCIÓN TEMPORAL
# ══════════════════════════════════════════════════════
st.markdown('<div class="section-title">📈 Evolución temporal</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Por región", "Por país", "Doble eje"])

with tab1:
    evol_region = (
        df_f.groupby(["year","region"])[variable_sel]
        .mean().reset_index()
    )
    fig_evol = px.line(
        evol_region, x="year", y=variable_sel,
        color="region", markers=True,
        labels={variable_sel: variable_sel, "year": "Año"},
        height=380
    )
    fig_evol.update_layout(xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig_evol, use_container_width=True)

with tab2:
    if len(paises_sel) == 0:
        st.warning("Selecciona al menos un país en el sidebar.")
    else:
        evol_pais = (
            df_f[df_f["country"].isin(paises_sel)]
            .groupby(["year","country"])[variable_sel]
            .mean().reset_index()
        )
        fig_pais = px.line(
            evol_pais, x="year", y=variable_sel,
            color="country", markers=True,
            labels={variable_sel: variable_sel, "year": "Año"},
            height=380
        )
        fig_pais.update_layout(xaxis=dict(tickmode="linear", dtick=1))
        st.plotly_chart(fig_pais, use_container_width=True)

with tab3:
    region_doble = st.selectbox(
        "Región para doble eje",
        options=regiones_sel if regiones_sel else regiones_disponibles
    )
    subset_doble = (
        df_f[df_f["region"] == region_doble]
        .groupby("date")[["avg_temperature","energy_consumption"]]
        .mean().reset_index()
    )
    fig_doble = make_subplots(specs=[[{"secondary_y": True}]])
    fig_doble.add_trace(go.Scatter(
        x=subset_doble["date"], y=subset_doble["avg_temperature"],
        name="Temperatura (°C)", line=dict(color="#E24B4A", width=1.5)
    ), secondary_y=False)
    fig_doble.add_trace(go.Scatter(
        x=subset_doble["date"], y=subset_doble["energy_consumption"],
        name="Consumo energético", line=dict(color="#065A82", width=1.5)
    ), secondary_y=True)
    fig_doble.update_layout(height=380, legend=dict(orientation="h", y=-0.2))
    fig_doble.update_yaxes(title_text="Temperatura (°C)", secondary_y=False)
    fig_doble.update_yaxes(title_text="Consumo energético", secondary_y=True)
    st.plotly_chart(fig_doble, use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════════════
# SECCIÓN 3 — COMPARATIVO POR PAÍS
# ══════════════════════════════════════════════════════
st.markdown('<div class="section-title">🏆 Comparativo por país</div>', unsafe_allow_html=True)

col_bar, col_box = st.columns(2)

with col_bar:
    ranking = (
        df_f.groupby(["country","region"])[variable_sel]
        .mean().reset_index()
        .sort_values(variable_sel, ascending=True)
    )
    fig_bar = px.bar(
        ranking, x=variable_sel, y="country",
        color="region", orientation="h",
        height=500,
        labels={variable_sel: variable_sel, "country": "País"}
    )
    media_global = df_f[variable_sel].mean()
    fig_bar.add_vline(
        x=media_global, line_dash="dash",
        line_color="black", line_width=1,
        annotation_text=f"Media: {media_global:.1f}",
        annotation_position="top right"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_box:
    fig_box = px.box(
        df_f, x="region", y=variable_sel,
        color="region", height=500,
        labels={variable_sel: variable_sel, "region": "Región"}
    )
    fig_box.update_layout(showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════════════
# SECCIÓN 4 — CORRELACIONES
# ══════════════════════════════════════════════════════
st.markdown('<div class="section-title">🔗 Análisis de correlaciones</div>', unsafe_allow_html=True)

col_heat, col_scatter = st.columns(2)

variables_num = [
    "avg_temperature","humidity","co2_emission","energy_consumption",
    "renewable_share","urban_population","industrial_activity_index","energy_price"
]

with col_heat:
    corr = df_f[variables_num].corr()
    fig_heat = px.imshow(
        corr, text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        height=420,
        title="Matriz de correlación"
    )
    fig_heat.update_layout(margin=dict(t=40, b=0))
    st.plotly_chart(fig_heat, use_container_width=True)

with col_scatter:
    st.markdown("**Scatter interactivo**")
    eje_x = st.selectbox("Eje X", options=variables_num, index=2)
    eje_y = st.selectbox("Eje Y", options=variables_num, index=3)

    r, p = stats.pearsonr(df_f[eje_x].dropna(), df_f[eje_y].dropna())

    fig_scatter = px.scatter(
        df_f.sample(min(3000, len(df_f)), random_state=42),
        x=eje_x, y=eje_y, color="region",
        opacity=0.5, trendline="ols",
        height=360,
        labels={eje_x: eje_x, eje_y: eje_y}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    col_r1, col_r2, col_r3 = st.columns(3)
    col_r1.metric("Pearson r", f"{r:.4f}")
    col_r2.metric("R²", f"{r**2:.4f}")
    col_r3.metric("p-valor", f"{p:.2e}")

st.markdown("---")

# ══════════════════════════════════════════════════════
# SECCIÓN 5 — RENOVABLES VS CO₂
# ══════════════════════════════════════════════════════
st.markdown('<div class="section-title">🌱 Renovables vs CO₂ vs Precio</div>', unsafe_allow_html=True)

resumen_burbuja = (
    df_f.groupby(["country","region"])
    .agg(
        renovable=("renewable_share","mean"),
        co2=("co2_emission","mean"),
        precio=("energy_price","mean"),
        consumo=("energy_consumption","mean")
    ).reset_index().round(2)
)

fig_burbuja = px.scatter(
    resumen_burbuja,
    x="renovable", y="precio",
    size="co2", color="region",
    text="country",
    title="% Renovable vs Precio energía (tamaño = CO₂)",
    labels={
        "renovable": "% Renovable promedio",
        "precio":    "Precio energía promedio",
        "co2":       "CO₂ promedio"
    },
    height=500, size_max=40
)
fig_burbuja.update_traces(textposition="top center", textfont_size=9)
st.plotly_chart(fig_burbuja, use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════════════
# SECCIÓN 6 — TABLA DE DATOS
# ══════════════════════════════════════════════════════
st.markdown('<div class="section-title">📋 Resumen por país</div>', unsafe_allow_html=True)

resumen_tabla = (
    df_f.groupby(["country","region"])
    .agg(
        temp_prom    =("avg_temperature","mean"),
        co2_prom     =("co2_emission","mean"),
        consumo_prom =("energy_consumption","mean"),
        renovable_pct=("renewable_share","mean"),
        precio_prom  =("energy_price","mean"),
        ind_prom     =("industrial_activity_index","mean")
    ).reset_index().round(2)
)
resumen_tabla.columns = [
    "País","Región","Temp. (°C)","CO₂ prom.",
    "Consumo prom.","% Renovable","Precio prom.","Índice ind."
]

st.dataframe(
    resumen_tabla,
    use_container_width=True,
    hide_index=True,
    column_config={
        "% Renovable": st.column_config.ProgressColumn(
            "% Renovable", min_value=0, max_value=35, format="%.1f%%"
        ),
        "CO₂ prom.": st.column_config.NumberColumn("CO₂ prom.", format="%.0f"),
    }
)

col_dl1, col_dl2 = st.columns([1,4])
with col_dl1:
    csv = resumen_tabla.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Descargar CSV",
        data=csv,
        file_name="resumen_paises.csv",
        mime="text/csv"
    )

st.markdown("---")

# ── Footer ─────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; color:#64748B; font-size:0.85rem; padding: 1rem 0'>
    <strong>Miguel Sierra</strong> · Talento Tech — Análisis de Datos · 2025 ·
    <a href='https://github.com/Miguel-sierra89/proyecto-clima-energia' target='_blank'>GitHub ↗</a>
</div>
""", unsafe_allow_html=True)

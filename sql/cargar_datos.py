import pandas as pd
from sqlalchemy import create_engine, text

# ── Configuración de conexión ──────────────────────────
USUARIO  = "root"
PASSWORD = "TalentoTech2"   # ← cambia esto por tu contraseña real
HOST     = "localhost"
PUERTO   = "3306"
BASE     = "clima_energia_global"

# ── Crear conexión ─────────────────────────────────────
engine = create_engine(
    f"mysql+pymysql://{USUARIO}:{PASSWORD}@{HOST}:{PUERTO}/{BASE}"
)

# ── Cargar y preparar el dataset ───────────────────────
df = pd.read_csv("data/dataset_limpio.csv", parse_dates=["date"])

regiones = {
    "Germany"       : "Europa",
    "France"        : "Europa",
    "United Kingdom": "Europa",
    "Italy"         : "Europa",
    "Spain"         : "Europa",
    "Sweden"        : "Europa",
    "Norway"        : "Europa",
    "Netherlands"   : "Europa",
    "Poland"        : "Europa",
    "Turkey"        : "Europa",
    "United States" : "America",
    "Canada"        : "America",
    "Mexico"        : "America",
    "Brazil"        : "America",
    "China"         : "Asia-Pacifico",
    "India"         : "Asia-Pacifico",
    "Japan"         : "Asia-Pacifico",
    "Indonesia"     : "Asia-Pacifico",
    "Australia"     : "Asia-Pacifico",
    "South Africa"  : "Africa"
}
df["region"] = df["country"].map(regiones)

# Formatear fecha como string para MySQL
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

# Eliminar columnas extra
df = df.drop(columns=["year", "month"], errors="ignore")

# Renombrar columnas al español
df = df.rename(columns={
    "date"                     : "fecha",
    "country"                  : "pais",
    "avg_temperature"          : "temperatura_promedio",
    "humidity"                 : "humedad",
    "co2_emission"             : "emision_co2",
    "energy_consumption"       : "consumo_energetico",
    "renewable_share"          : "participacion_renovable",
    "urban_population"         : "poblacion_urbana",
    "industrial_activity_index": "indice_actividad_ind",
    "energy_price"             : "precio_energia"
})

# Verificar los 20 países antes de cargar
print("Países detectados en el CSV:")
for pais, n in df["pais"].value_counts().sort_index().items():
    print(f"  {pais:<25} {n} registros")
print(f"\nTotal filas a cargar: {len(df):,}")

# ── Cargar a MySQL ─────────────────────────────────────
print("\n⏳ Cargando datos a MySQL...")
df.to_sql(
    name      = "registros_clima_energia",
    con       = engine,
    if_exists = "append",
    index     = False,
    chunksize = 1000
)

# ── Verificación final ─────────────────────────────────
with engine.connect() as conn:
    total = conn.execute(
        text("SELECT COUNT(*) FROM registros_clima_energia")
    ).fetchone()[0]
    print(f"✅ Verificación MySQL: {total:,} registros en la tabla")

    print("\nRegistros por país en MySQL:")
    resultado = conn.execute(
        text("""SELECT pais, COUNT(*) as registros
                FROM registros_clima_energia
                GROUP BY pais
                ORDER BY pais""")
    ).fetchall()
    for row in resultado:
        print(f"  {row[0]:<25} {row[1]} registros")
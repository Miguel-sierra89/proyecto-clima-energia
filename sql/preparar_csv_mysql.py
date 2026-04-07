import pandas as pd

df = pd.read_csv("../data/dataset_limpio.csv", parse_dates=["date"])

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

# Formatear fecha como string para MySQL
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

# Eliminar columnas extra
df = df.drop(columns=["year","month"], errors="ignore")

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

# Guardar CSV listo para MySQL
df.to_csv("../data/datos_para_mysql.csv", index=False)
print(f"✅ CSV generado: data/datos_para_mysql.csv")
print(f"   Filas: {len(df):,} | Columnas: {list(df.columns)}")
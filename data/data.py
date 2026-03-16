import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# CSV/TSV laden
df = pd.read_csv("raw/Occurrence.tsv", sep='\t', low_memory=False)  # tsv = Tab-Separated Values

# Nur Zeilen mit Art, Datum, Koordinaten
df = df.dropna(subset=['scientificName', 'eventDate', 'decimalLatitude', 'decimalLongitude'])

# Datum in datetime umwandeln
df['eventDate'] = pd.to_datetime(df['eventDate'])
df['year'] = df['eventDate'].dt.year

# Mapping wissenschaftlicher Name → deutscher Name
name_map = {
    "Larus novaehollandiae": "Silbermöwe",
    "Sterna bergii": "Weißbrustseeschwalbe",
    "Egretta sacra": "Rotschnabelreiher",
    "Sterna sumatrana": "Sumatra-Seeschwalbe",
    "Sula leucogaster": "Braunschwingen-Tölpel",
    "Anous minutus": "Schwarzfußtölpel",
    "Onychoprion anaethetus": "Graukopftölpel",
    "Anous stolidus": "Noddi-Tölpel",
    "Fregata ariel": "Fregattvogel",
    "Sterna bengalensis": "Bengalseeschwalbe"
}

# scientificName umbenennen: wissenschaftlicher + deutscher Name
df["scientificName"] = df["scientificName"].apply(
    lambda x: f"{x} ({name_map[x]})" if x in name_map else x
)


# Matplotlib: Statische Karte
plt.figure(figsize=(10,10))
sc = plt.scatter(
    x=df["decimalLongitude"],
    y=df["decimalLatitude"],
    c=df["sst"],        # Farbe = SST
    cmap="coolwarm",    # Farbpalette von kalt → warm
    s=200,              # Punktgröße
    alpha=0.7
)

cbar = plt.colorbar(sc)
cbar.set_label("Sea Surface Temperature (°C)", fontsize=18)
cbar.ax.tick_params(labelsize=17)

plt.xlabel("Longitude", fontsize=18)
plt.ylabel("Latitude", fontsize=18)
plt.title("Seabird Observations Colored by Sea Surface Temperature (1991-1996)", fontsize=20)
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)
plt.show()

# ------------------------------
# Plotly: interaktive Karte
# ------------------------------
fig = px.scatter(
    df,
    x="decimalLongitude",
    y="decimalLatitude",
    color="sst",
    hover_name="scientificName",
    color_continuous_scale="Viridis",
    labels={"sst":"Sea Surface Temperature (°C)"},
    title="Seabird Observations – Great Barrier Reef (Interactive) (1991-1996)"
)

fig.update_layout(
    title=dict(
        text="Seabird Observations – Great Barrier Reef (Interactive) (1991-1996)",
        x=0.5,  # Titel horizontal mittig
        font=dict(size=20)
    ),
    xaxis_title="Longitude",
    yaxis_title="Latitude",
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    coloraxis_colorbar=dict(
        title=dict(
            text="Sea Surface Temperature (°C)",
            font=dict(size=16),
            side="right"
        ),
        tickfont=dict(size=14),
        len=0.8,
        thickness=20
    )
)

fig.show()
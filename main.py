import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from configparser import ConfigParser
import sys


# Settings
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 100)
# CONSTANTS
CURRENT_PATH = os.getcwd()
FILE_PATH = os.path.join(CURRENT_PATH, "Nice_Places.csv")
ENV_PATH = os.path.join(CURRENT_PATH, ".env")


# Transforms abbreviations to words
def preprocess_horaires(horaires):
    week_days = {
        "Lu": "Lundi",
        "Ma": "Mardi",
        "Me": "Mercredi",
        "Je": "Jeudi",
        "Ve": "Vendredi",
        "Sa": "Samedi",
        "Di": "Dimanche",
        "Toute": "Chaque jour"
    }
    days_hours = horaires.split('-')
    assert (len(days_hours) % 3 == 0), ("Wrong data format should be: Day1,Day2,...Dayn-hours:minutes-hours:minutes"
                                        "-Dayn+1-hours:minutes-hours:minutes")
    days = ""
    for i in range(0, len(days_hours), 3):
        days += "".join([f"{week_days[key]}\n" for key in days_hours[i].split(",") if key in week_days])
        days += days_hours[i + 1] + "-" + days_hours[i + 2]+"\n"
    return days


def click(df):
    config = ConfigParser()
    config.read(ENV_PATH)
    fig = go.Figure(go.Scattermapbox(
        lat=df["Lat"],
        lon=df["Lon"],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        hovertext=df["Horaires"],
        text=['Nice'],
    ))
    fig.update_layout(clickmode='event+select',
                      mapbox={"center":go.layout.mapbox.Center(lat=df["Lat"].iloc[0],lon=df["Lon"].iloc[0]),
                              "accesstoken" : config["MAPBOX"]["MAPBOX_TOKEN"],
                              'zoom': 15,
                              },
                      margin=dict(l=0, r=0, t=0, b=0)
                      )
    fig.show()


def main(mode):
    # Reading csv file
    df = pd.read_csv(FILE_PATH, delimiter=";", encoding='latin1')
    # Data Preprocessing
    df[["Lat", "Lon"]] = df["LatLon"].str.split(',', expand=True)
    df["Lat"] = df["Lat"].astype("float64")
    df["Lon"] = df["Lon"].astype("float64")
    df["Horaires"] = df["Horaires"].apply(preprocess_horaires)


    print(mode)
    if mode[1] == "interactable":
        click(df)
        return

    # Reading token
    config = ConfigParser()
    config.read(ENV_PATH)
    px.set_mapbox_access_token(config["MAPBOX"]["MAPBOX_TOKEN"])

    # Visualisation
    fig = px.scatter_mapbox(df, lat="Lat", lon="Lon", color="Catégorie", text="Nom", hover_data=["Horaires","Lien"],
                            color_continuous_scale=px.colors.cyclical.Phase, size_max=25, zoom=15,
                            title="Carte des lieux à visiter")
    fig.show()


if __name__ == '__main__':
    main(sys.argv)

import os
import pandas as pd
import plotly.express as px
from configparser import ConfigParser

# Settings
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 100)
# CONSTANTS
CURRENT_PATH = os.getcwd()
FILE_PATH = os.path.join(CURRENT_PATH, "Nice_Places.csv")
ENV_PATH = os.path.join(CURRENT_PATH, ".env")


def main():
    # Reading token
    config = ConfigParser()
    config.read(ENV_PATH)
    px.set_mapbox_access_token(config["MAPBOX"]["MAPBOX_TOKEN"])
    # Reading csv file
    df = pd.read_csv(FILE_PATH, delimiter=";", encoding='latin1')
    # Data Preprocessing
    df[["Lat", "Lon"]] = df["LatLon"].str.split(',', expand=True)
    df["Lat"] = df["Lat"].astype("float64")
    df["Lon"] = df["Lon"].astype("float64")

    #TODO Parse Horaires

    # Visualisation
    fig = px.scatter_mapbox(df, lat="Lat", lon="Lon", color="Catégorie", text="Nom", hover_data="Lien",
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=15)
    fig.show()


if __name__ == '__main__':
    main()

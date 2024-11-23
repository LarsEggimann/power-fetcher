#!/usr/bin/env python3


from nicegui import ui
import pandas as pd
from pathlib import Path
import urllib.request

root = Path(__file__).parent.parent

class PowerPlot:
    def __init__(self):
        
        self.data = pd.read_csv(root / "data" / "data.csv")

        self.request = None

        self.init_data_fetcher()


    def init_data_fetcher(self):
        ui.timer(30, self.fetch_and_append_data)

    async def fetch_and_append_data(self):
        try:
            response = urllib.request.urlopen("http://192.168.1.97/")
        except:
            response = None
            print("Could not fetch data")

        if response:
            print(response.read())


    def create_ui(self):
        ui.label("Power Consumption")
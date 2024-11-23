#!/usr/bin/env python3


from nicegui import ui
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import urllib.request
import csv

root = Path(__file__).parent.parent

class PowerPlot:
    def __init__(self):

        self.refresh_interval = 5

        self.data_file = root / "data" / "data.csv"
        
        self.data = pd.read_csv(self.data_file)

        self.request = None

        self.init_data_fetcher()

        self.plot_nicegui: ui.plotly = None

        self.plot_plotly: go.Figure = px.line(self.data, x="time", y="power")
        self.plot_plotly.update_layout(
            title="Power Consumption",
            xaxis_title="Time",
            yaxis_title="Power [W]",
            template="seaborn",
            xaxis=dict(rangeslider_visible=True),
        )

        self.response_string = None


    def init_data_fetcher(self):
        ui.timer(self.refresh_interval, self.fetch_and_append_data)

    async def fetch_and_append_data(self):
        try:
            response = urllib.request.urlopen("http://192.168.1.97/")
        except:
            response = None
            print("Could not fetch data")

        if response:
            self.response_string = response.read().decode("utf-8")

            # match the pattern <tr><td>P</td><td>xxx</td> and find the value of xxx
            power = int(self.response_string.split("<tr><td>P</td><td>")[1].split("</td>")[0])

            time = pd.Timestamp.now()

            # append the new data to csv file
            with open(self.data_file, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([time, power])

    def refresh_plot(self):
        self.data = pd.read_csv(self.data_file)
        self.plot_plotly.update_traces(x=self.data["time"], y=self.data["power"])
        self.plot_nicegui.update()
        self.render_html_response.refresh()

    @ui.refreshable
    def render_html_response(self):
        if self.response_string:
            ui.html(self.response_string)


    def create_ui(self):
        ui.label("Power Consumption")

        with ui.grid(columns=1, rows=1).classes("w-full justify-center"):
            self.plot_nicegui = ui.plotly(self.plot_plotly).classes(replace="w-full")

        timer = ui.timer(self.refresh_interval, self.refresh_plot)

        # add a switch to enable/disable auto refresh
        def on_switch_change(e):
            timer.active = e.value
            
        ui.switch("Auto Refresh", value=timer.active, on_change=on_switch_change)

        self.render_html_response()

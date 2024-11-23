#!/usr/bin/env python3


from nicegui import ui, app
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import urllib.request
import csv

root = Path(__file__).parent.parent

def datetime_to_timestamp(datetime):
    return pd.Timestamp(datetime).timestamp()

class PowerPlot:
    def __init__(self):

        self.refresh_interval = app.storage.general.get("refresh_interval", 30)

        self.data_file = root / "data" / "data.csv"
        
        self.data = pd.read_csv(self.data_file)

        self.request = None

        self.data_fetch_timer = ui.timer(self.refresh_interval, self.fetch_and_append_data)

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

        self.energy_consumption = 0
        self.current_power = 0
        self.total_time_interval = 0

    async def fetch_and_append_data(self):
        try:
            response = urllib.request.urlopen("http://192.168.1.97/")
        except:
            response = None
            print("Could not fetch data")

        if response:
            self.response_string = response.read().decode("utf-8")

            # match the pattern <tr><td>P</td><td>xxx</td> and find the value of xxx
            self.current_power = int(self.response_string.split("<tr><td>P</td><td>")[1].split("</td>")[0])

            time = pd.Timestamp.now()

            try:
                # append the new data to csv file
                with open(self.data_file, "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([time, self.current_power])
            except:
                print("Could not write to file")

    def refresh_plot_and_data(self):
        self.data = pd.read_csv(self.data_file)
        self.plot_plotly.update_traces(x=self.data["time"], y=self.data["power"])
        self.plot_nicegui.update()
        self.render_html_response.refresh()

        self.energy_consumption = np.trapezoid(self.data["power"], x=list(map(datetime_to_timestamp, self.data['time']))) # Ws
        self.energy_consumption /= 3600 # Wh
        self.energy_consumption /= 1000 # kWh

        self.total_time_interval = pd.Timestamp(self.data["time"].iloc[-1]) - pd.Timestamp(self.data["time"].iloc[0])

    @ui.refreshable
    def render_html_response(self):
        if self.response_string:
            ui.html(self.response_string)


    def create_ui(self):
        ui.label("Power Consumption")

        with ui.grid(columns=1, rows=1).classes("w-full justify-center"):
            self.plot_nicegui = ui.plotly(self.plot_plotly).classes(replace="w-full")

        plot_timer = ui.timer(self.refresh_interval, self.refresh_plot_and_data)

        # add a switch to enable/disable auto refresh
        def on_switch_change(e):
            plot_timer.active = e.value
        
        def on_refresh_interval_change(e):
            self.refresh_interval = e.value
            app.storage.general["refresh_interval"] = self.refresh_interval
            plot_timer.interval = self.refresh_interval
            self.data_fetch_timer.interval = self.refresh_interval

        
        with ui.row(wrap=False).classes("w-full justify-center items-center m-10 p-10"):
            ui.switch("Auto Refresh", value=plot_timer.active, on_change=on_switch_change)
            ui.number("Refresh Interval [s]", value=self.refresh_interval, min=1, max=60, step=1, on_change=on_refresh_interval_change).classes("w-28")
        
        with ui.row(wrap=False).classes("w-full justify-center items-center m-10 p-10"):
            ui.label().bind_text_from(self, "current_power", backward=lambda x: f"Current Power: {x} W")
            ui.label(" -----> ")
            ui.label().bind_text_from(self, "energy_consumption", backward=lambda x: f"Energy Consumption since start of recording: {x:.5f} kWh")
            ui.label(" - ")
            ui.label().bind_text_from(self, "total_time_interval", backward=lambda x: f"Total Time Interval: {x}")
            
        with ui.expansion("Raw Data", icon='analytics').classes("w-full justify-center items-center"):
            self.render_html_response()

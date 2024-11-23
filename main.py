#!/usr/bin/env python3

from pathlib import Path
from components import create_layout
from nicegui import ui
from components import PowerPlot

pp = PowerPlot()

@ui.page("/")
async def home():
    create_layout()
    pp.create_ui()

@ui.page("/main")
async def redir():
    ui.navigate.to("/")


if __name__ in {"__main__", "__mp_main__"}:

    ui.navigate.to("/")

    ui.run(
        reload=True,
        show=False,
        on_air=None,
        host="0.0.0.0",
        title="Kommune Power Consumption",
        favicon=str(Path(__file__).parent / "static" / "icon.svg"),
        port=50051,
        storage_secret='crazy_secret'
    )

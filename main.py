#!/usr/bin/env python3

from pathlib import Path
from components import create_layout
from nicegui import ui
from components import PowerPlot

pp = PowerPlot()

@ui.page("/main")
async def main():
    create_layout()
    pp.create_ui()


if __name__ in {"__main__", "__mp_main__"}:

    ui.navigate.to("/main")

    ui.run(
        reload=True,
        show=False,
        on_air=None,
        host="0.0.0.0",
        title="Kommune Power Consumption",
        favicon=str(Path(__file__).parent / "static" / "icon.ico"),
        port=50051,
    )

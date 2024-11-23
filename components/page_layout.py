#!/usr/bin/env python3
import asyncio
import logging
import logging.config
from pathlib import Path
from nicegui import app, ui

import os


def create_layout():

    with ui.left_drawer(value=False).props("bordered") as left_drawer:
        ui.label("Navigation")

        ui.separator()

        ui.link("Main", "/main")


    with ui.right_drawer(value=False).props("bordered width=450") as right_drawer:
        ui.label("Settings")


    with ui.header(elevated=False).classes("flex justify-between"):
        ui.button(on_click=left_drawer.toggle, icon="menu").props("flat color=white")
        
        with ui.link(target="/main").tooltip("Go Home!"):
            ui.button(text="Kommune Power Consumption").props("flat color=white").classes("text-xl")

        ui.button(on_click=right_drawer.toggle, icon="settings").props(
            "flat color=white"
        )

    with ui.footer().classes("flex justify-between "):

        ui.label("Kommune Power Consumption - Show your power!")

        with ui.row().classes("items-center"):
            ui.label("Made with")
            ui.button(" ❤️ ", color=None).tooltip(
                "Whats this?"
            )
            ui.label("by Lars Eggimann")

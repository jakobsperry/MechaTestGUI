import tkinter as tk
from tkinter import ttk

def get_ui_style():
    """Return a dictionary with UI styles and common dimensions."""
    style = ttk.Style()
    style.theme_use("clam")

    # Button Styles
    style.configure("primary.TButton",
                    relief="flat",
                    padding=(10, 1),
                    font=("Helvetica", 12),
                    foreground="white",
                    background="#4880e8")
    style.map("primary.TButton", background=[("active", "#4880e8")])

    style.configure("secondary.TButton",
                    relief="flat",
                    padding=(10, 1),
                    font=("Helvetica", 12),
                    foreground="black",
                    background="white")
    style.map("secondary.TButton", background=[("active", "#white")])

    style.configure("start.TButton",
                    relief="flat",
                    padding=(10, 12),
                    font=("Helvetica", 12),
                    foreground="white",
                    background="#4bdb4b")
    style.map("start.TButton", background=[("active", "#4bdb4b")])

    # Label Styles
    style.configure("heading.TLabel",
                    font=("Helvetica", 12),
                    foreground="gray",
                    background="#ebebeb")

    # Common UI dimensions

    padding = 10
    textbox_width = 32
    button_width = int(textbox_width / 2 - 3)
    button_width2 = int(textbox_width / 3 - 3)
    component_width = 4

    return {
        "style": style,
        "padding": padding,
        "textbox_width": textbox_width,
        "button_width": button_width,
        "button_width2": button_width2,
        "component_width": component_width
    }

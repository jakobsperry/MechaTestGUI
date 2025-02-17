import tkinter as tk
from tkinter import ttk

import numpy as np

from style import get_ui_style

class SetupTestPage(tk.Frame):
    def __init__(self, parent, controller, config_data):

        super().__init__(parent)
        self.config_data = config_data

        self.controller = controller
        self.root = self.controller.root

        ui_style = get_ui_style()
        self.style = ui_style["style"]

        # Assign UI dimension variables
        self.padding = ui_style["padding"]
        self.textbox_width = ui_style["textbox_width"]
        self.button_width = ui_style["button_width"]
        self.button_width2 = ui_style["button_width2"]
        self.component_width = ui_style["component_width"]



        self.robot_label = ttk.Label(self, text="Robot IP:", style="heading.TLabel", anchor="w")
        self.robot_label.pack(pady=2, padx=0, anchor="w")

        self.robot_ip_var = tk.StringVar()
        self.robot_ip_text_entry = ttk.Entry(self, textvariable=self.robot_ip_var, width=self.textbox_width)
        self.robot_ip_text_entry.pack(side=tk.TOP, pady=2, anchor="w", padx=self.padding)
        self.robot_ip_text_entry.insert(0, self.controller.config_data["Robot IP"])

        
        self.sensor_port_label = ttk.Label(self, text="Sensor Port:", style="heading.TLabel", anchor="w")
        self.sensor_port_label.pack(pady=2, padx=0, anchor="w")

        self.sensor_port_var = tk.StringVar()
        self.sensor_port_entry = ttk.Entry(self, textvariable=self.sensor_port_var, width=self.textbox_width)
        self.sensor_port_entry.pack(side=tk.TOP, pady=2, anchor="w", padx=self.padding)
        self.sensor_port_entry.insert(0, self.controller.config_data["Sensor Port"])

        self.test_button = ttk.Button(self, text="Connect", command=self.controller.test.connect, style="primary.TButton", width=int(self.textbox_width -3))
        self.test_button.pack(side=tk.TOP, pady=2, padx=self.padding, fill=tk.X)



        # -------------------------------
        # Start Pose - Textboxes with Labels
        # -------------------------------

        
        frame = tk.Frame(self)
        frame.pack(padx=40, pady=20)

        self.start_pose_label = ttk.Label(self, text="Start Pose:", style="heading.TLabel", anchor="w")
        self.start_pose_label.pack(pady=2, padx=0, anchor="w")

        self.start_pose_frame = tk.Frame(self)
        self.start_pose_frame.pack(side=tk.TOP, padx=1, pady=1, fill=tk.X)

        self.start_pose_entries = []
        for i in range(6):
            entry = ttk.Entry(self.start_pose_frame, width=5)
            entry.grid(row=1, column=i, padx=1, pady=2)
            entry.insert(0, self.config_data["Start Pose"][i])
            self.start_pose_entries.append(entry)

        # -------------------------------
        # Test Motion - Textboxes
        # -------------------------------
        self.test_vector_label = ttk.Label(self, text="Test Vector:", style="heading.TLabel", anchor="w")
        self.test_vector_label.pack(pady=2, padx=0, anchor="w")

        self.test_motion_frame = tk.Frame(self)
        self.test_motion_frame.pack(side=tk.TOP, padx=1, pady=1, fill=tk.X)

        self.test_motion_entries = []
        for i in range(6):
            entry = ttk.Entry(self.test_motion_frame, width=5)
            entry.grid(row=1, column=i, padx=1, pady=2)
            entry.insert(0, self.config_data["Test Vector"][i])
            self.test_motion_entries.append(entry)

        # -------------------------------
        # Retract Vector - Textboxes
        # -------------------------------
        self.retract_vector_label = ttk.Label(self, text="Retract Vector:", style="heading.TLabel", anchor="w")
        self.retract_vector_label.pack(pady=2, padx=0, anchor="w")

        self.retract_vector_frame = tk.Frame(self)
        self.retract_vector_frame.pack(side=tk.TOP, padx=1, pady=1, fill=tk.X)

        self.retract_vector_entries = []
        for i in range(6):
            entry = ttk.Entry(self.retract_vector_frame, width=5)
            entry.grid(row=1, column=i, padx=1, pady=2)
            entry.insert(0, self.config_data["Retract Vector"][i])
            self.retract_vector_entries.append(entry)



    def get_start_pose_values(self):
        """Return the values from the start pose text boxes as a numpy array of floats."""
        values = []
        for entry in self.start_pose_entries:
            try:
                values.append(float(entry.get()))
            except ValueError:
                # If conversion fails, default to 0.0
                values.append(0.0)
        return np.array(values)


    def get_test_vector_values(self):
        """Return the values from the test vector text boxes as a numpy array of floats."""
        values = []
        for entry in self.test_motion_entries:
            try:
                values.append(float(entry.get()))
            except ValueError:
                # If conversion fails, default to 0.0
                values.append(0.0)
        return np.array(values)
    

    def get_retract_vector_values(self):
        """Return the values from the retract vector text boxes as a numpy array of floats."""
        values = []
        for entry in self.retract_vector_entries:
            try:
                values.append(float(entry.get()))
            except ValueError:
                # If conversion fails, default to 0.0
                values.append(0.0)
        return np.array(values)
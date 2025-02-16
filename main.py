import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "resources"))

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from functools import partial
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from test_controller import Test
import csv

import csv
from datetime import datetime

import json


class SimpleApp:
    def __init__(self, root):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(base_dir)
    
        self.root = root
        self.root.title("Noodle Test")

        style = ttk.Style()
        style.theme_use("clam")


        style.configure("primary.TButton",
            relief="flat",
            padding=(10, 1),
            font=("Helvetica", 12),
            foreground = "white",
            background="#4880e8")
        style.map("primary.TButton", background=[("active", "#4880e8")])


        style.configure("secondary.TButton",
            relief="flat",
            padding=(10, 1),
            font=("Helvetica", 12),
            foreground = "black",
            background="white",)
        style.map("secondary.TButton", background=[("active", "#white")])


        style.configure("start.TButton",
            relief="flat",
            padding=(10, 12),
            font=("Helvetica", 12),
            foreground = "white",
            background="#4bdb4b")
        style.map("start.TButton", background=[("active", "#4bdb4b")])
       

        style.configure("heading.TLabel",
            font=("Helvetica", 12,),
            fg="gray",
            background="#ebebeb")


        # Example "test" object for data collection
        self.test = Test()
        self.testActive = False
        self.alignActive = False
        self.jogActive = False

        self.fileName = ""
        self.test_name = ""

        self.data = np.zeros((2000, 7))

        self.config_data = {
            "Test Name": "",
            "Start Pose": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Retract Vector": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Test Vector": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Align Axis": [1, 1, 1, 1, 1, 1]
        }

        self.loadConfigFile("resources/TestConfigs/autosave.json")
        
        self.padding = 10

        self.textbox_width = 32
        self.button_width = int(self.textbox_width/2-3)
        self.button_width2 = int(self.textbox_width/3-3)
        self.component_width = 4
        

        # -------------------------------
        # 1) Frame: LEFT
        # -------------------------------
        leftframe = tk.Frame(root, background="#ebebeb")
        leftframe.pack(side=tk.LEFT, padx=0, pady=2)

        # -------------------------------
        # 1) Frame: LEFT Padded
        # -------------------------------
        frame = tk.Frame(leftframe)
        frame.pack(padx=40, pady=20)

        self.name_label = ttk.Label(frame, text="Test Name:", style="heading.TLabel", anchor="w")
        self.name_label.pack(pady=2, padx=0, anchor="w")


        self.text_var = tk.StringVar()
        self.text_entry = ttk.Entry(frame, textvariable=self.text_var, width=self.textbox_width)
        self.text_entry.pack(side=tk.TOP, pady=2, anchor="w", padx=self.padding)
        self.text_entry.insert(0, self.config_data["Test Name"])
        self.text_var.trace_add("write", self.check_textbox)
        
        # -------------------------------
        # 1) Frame: Config Buttons
        # -------------------------------

        config_buttons_container = tk.Frame(frame)
        config_buttons_container.pack(side=tk.TOP, padx=0, pady=2)

        # Create sub-frames for left and right
        save_congig_frame = tk.Frame(config_buttons_container)
        save_congig_frame.grid(row=0, column=0, padx=0, pady=2, sticky="ew")  # Use grid and fill horizontally

        load_congig_frame = tk.Frame(config_buttons_container)
        load_congig_frame.grid(row=0, column=1, padx=0, pady=2, sticky="ew")  # Same here, align horizontally

        # Remove padding and use pady=2 for the pack inside each button
        self.save_button = ttk.Button(load_congig_frame, text="Import Config", command=self.importConfig, style="primary.TButton", width=self.button_width)
        self.save_button.pack(side=tk.TOP, pady=2, padx=self.padding)

        self.save_button = ttk.Button(save_congig_frame, text="Save Config", command=partial(self.saveConfig, False), style="primary.TButton", width=self.button_width)
        self.save_button.pack(side=tk.TOP, pady=2, padx=self.padding)


        # -------------------------------
        # Start Pose - Textboxes with Labels
        # -------------------------------

        self.padFrame = tk.Frame(frame)
        self.padFrame.pack(pady=15, padx=0)

        self.start_pose_label = ttk.Label(frame, text="Start Pose:", style="heading.TLabel", anchor="w")
        self.start_pose_label.pack(pady=2, padx=0, anchor="w")

        self.start_pose_frame = tk.Frame(frame)
        self.start_pose_frame.pack(side=tk.TOP, padx=1, pady=1, fill=tk.X)

        # List of labels to display above the entries
        self.start_pose_entries = []
        for i in range(6):
            entry = ttk.Entry(self.start_pose_frame, width=5)
            entry.grid(row=1, column=i, padx=1, pady=2)
            entry.insert(0, self.config_data["Start Pose"][i])
            self.start_pose_entries.append(entry)


        # -------------------------------
        # 3) Test Motion - Textboxes (Horizontally aligned)
        # -------------------------------

        self.padFrame = tk.Frame(frame)
        self.padFrame.pack(pady=2, padx=0)

        self.test_vector_label = ttk.Label(frame, text="Test Vector:", style="heading.TLabel", anchor="w")
        self.test_vector_label.pack(pady=2, padx=0, anchor="w")


        self.test_motion_frame = tk.Frame(frame)
        self.test_motion_frame.pack(side=tk.TOP, padx=1, pady=1, fill=tk.X)

        self.test_motion_entries = []
        for i in range(6):
            entry = ttk.Entry(self.test_motion_frame, width=5)
            entry.grid(row=1, column=i, padx=1, pady=2)
            entry.insert(0, self.config_data["Test Vector"][i])
            self.test_motion_entries.append(entry)



        # -------------------------------
        # 3) Retract Vector
        # -------------------------------

        self.padFrame = tk.Frame(frame)
        self.padFrame.pack(pady=2, padx=0)

        self.retract_vector_label = ttk.Label(frame, text="Retract Vector:", style="heading.TLabel", anchor="w")
        self.retract_vector_label.pack(pady=2, padx=0, anchor="w")


        self.retract_vector_frame = tk.Frame(frame)
        self.retract_vector_frame.pack(side=tk.TOP, padx=1, pady=1, fill=tk.X)

        self.retract_vector_entries = []
        for i in range(6):
            entry = ttk.Entry(self.retract_vector_frame, width=5)
            entry.grid(row=1, column=i, padx=1, pady=2)
            entry.insert(0, self.config_data["Retract Vector"][i])
            self.retract_vector_entries.append(entry)




        # -------------------------------
        # 1) Go To Frame
        # -------------------------------

        self.padFrame = tk.Frame(frame)
        self.padFrame.pack(pady=15, padx=0)

        self.goto_vector_label = ttk.Label(frame, text="Go To:", style="heading.TLabel", anchor="w")
        self.goto_vector_label.pack(pady=2, padx=0, anchor="w")

        config_goto_container = tk.Frame(frame)
        config_goto_container.pack(side=tk.TOP, padx=0, pady=2)

        # Create sub-frames for left and right
        home_frame = tk.Frame(config_goto_container)
        home_frame.grid(row=0, column=0, padx=0, pady=2, sticky="ew")  # Use grid and fill horizontally

        retract_frame = tk.Frame(config_goto_container)
        retract_frame.grid(row=0, column=1, padx=0, pady=2, sticky="ew")  # Same here, align horizontally
        
        test_frame = tk.Frame(config_goto_container)
        test_frame.grid(row=0, column=2, padx=0, pady=2, sticky="ew")  # Same here, align horizontally

        
        self.home_button = ttk.Button(home_frame, text="Home", command=self.zeroRobotJoints, style="secondary.TButton", width=self.button_width2)
        self.home_button.pack(side=tk.TOP, pady=2, padx=self.padding, fill=tk.X)
        
        self.retract_button = ttk.Button(retract_frame, text="Retract", command=self.goToRetract, style="secondary.TButton", width=self.button_width2)
        self.retract_button.pack(side=tk.TOP, pady=2, padx=self.padding, fill=tk.X)

        self.test_button = ttk.Button(test_frame, text="Test", command=self.moveToStart, style="secondary.TButton", width=self.button_width2)
        self.test_button.pack(side=tk.TOP, pady=2, padx=self.padding, fill=tk.X)

        self.test_button = ttk.Button(frame, text="Reset Errors", command=self.moveToStart, style="primary.TButton", width=int(self.textbox_width -3))
        self.test_button.pack(side=tk.TOP, pady=2, padx=self.padding, fill=tk.X)

       
    

        # -------------------------------
        # 4) Align Axis 
        # -------------------------------

        self.padFrame = tk.Frame(frame)
        self.padFrame.pack(pady=15, padx=0)
        
        self.goto_vector_label = ttk.Label(frame, text="Align:", style="heading.TLabel", anchor="w")
        self.goto_vector_label.pack(pady=2, padx=0, anchor="w")

        self.align_axis_frame = tk.Frame(frame)
        self.align_axis_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        # Create checkboxes for each axis in a single row.
        self.align_vars = {}  # We'll store the IntVars in a dictionary.
        for i, axis in enumerate(["X", "Y", "Z", "U", "V", "W"]):
            var = tk.IntVar(value=self.config_data["Align Axis"][i])
            self.align_vars[axis] = var
            chk = tk.Checkbutton(self.align_axis_frame, text=axis, variable=var)
            chk.grid(row=0, column=i, padx=6, pady=2)

        self.align_button = ttk.Button(frame, text="Align", command=self.align, style="primary.TButton", width=int(self.textbox_width -3))
        self.align_button.pack(side=tk.TOP, pady=1, fill=tk.X)
            


        # -------------------------------
        # Axis Controls
        # -------------------------------

        self.padFrame = tk.Frame(frame)
        self.padFrame.pack(pady=5, padx=0)

        self.axis_controls_frame = tk.Frame(frame)
        self.axis_controls_frame.pack(side=tk.TOP, padx=0, pady=0, fill=tk.X)

        axes = ["X", "Y", "Z", "U", "V", "W"]
        self.axis_buttons = {}

        # Row 0: Axis labels
        for i, axis in enumerate(axes):
            lbl = ttk.Label(self.axis_controls_frame, text=axis, style="heading.TLabel", anchor="center")
            lbl.grid(row=0, column=i, padx=1, pady=2)

        # Row 1: Plus buttons
        for i, axis in enumerate(axes):
            plus_button = ttk.Button(self.axis_controls_frame, text="+", width=3, style="secondary.TButton")
            plus_button.grid(row=1, column=i, padx=1, pady=2)
            plus_button.bind("<ButtonPress-1>", lambda event, idx=i: self.jogRobot(idx, +1))
            plus_button.bind("<ButtonRelease-1>", lambda event: self.stopJog())
            self.axis_buttons[axis] = {"plus": plus_button}

        # Row 2: Minus buttons
        for i, axis in enumerate(axes):
            minus_button = ttk.Button(self.axis_controls_frame, text="-", width=3, style="secondary.TButton")
            minus_button.grid(row=2, column=i, padx=1, pady=2)
            minus_button.bind("<ButtonPress-1>", lambda event, idx=i: self.jogRobot(idx, -1))
            minus_button.bind("<ButtonRelease-1>", lambda event: self.stopJog())
            self.axis_buttons[axes[i]]["minus"] = minus_button


        # -------------------------------
        # 1) Frame: Test/Data Buttons
        # -------------------------------
        
        self.padFrame = tk.Frame(frame)
        self.padFrame.pack(pady=20, padx=0)


        test_buttons_container = tk.Frame(frame)
        test_buttons_container.pack(side=tk.TOP, padx=0, pady=2)

        # Create sub-frames for left and right
        start_test_frame = tk.Frame(test_buttons_container)
        start_test_frame.grid(row=0, column=0, padx=0, pady=2, sticky="ew")  # Use grid and fill horizontally

        save_data_frame = tk.Frame(test_buttons_container)
        save_data_frame.grid(row=0, column=1, padx=0, pady=2, sticky="ew")  # Same here, align horizontally


        self.clear_button = ttk.Button(start_test_frame, text="Clear Graph", style="secondary.TButton", command=self.clearGraph,width=self.button_width)
        self.clear_button.pack(side=tk.TOP, pady=2, padx=self.padding, fill=tk.X)

        self.save_button = ttk.Button(save_data_frame, text="Save Test Data", command=self.saveData, style="secondary.TButton", width=self.button_width)
        self.save_button.pack(side=tk.TOP, pady=2, padx=self.padding,fill=tk.X)


        self.start_button = ttk.Button(frame, text="Start Test", command=self.start_test, style="start.TButton", width=int(self.textbox_width -3))
        self.start_button.pack(side=tk.TOP, pady=2, padx=self.padding, fill=tk.X)

        self.stop_button = ttk.Button(frame, text="Stop Test", command=self.stop_test, style="primary.TButton", width=int(self.textbox_width -3))
        self.stop_button.pack(side=tk.TOP, pady=2, padx=self.padding, fill=tk.X)


        # -------------------------------
        # 2) Figure and initial plots
        # -------------------------------


        self.dataFrame = tk.Frame(root, bg="white")
        self.dataFrame.pack(side=tk.RIGHT)


        # -------------------------------
        # Current Pose Display - Uneditable text boxes
        # -------------------------------
    

        self.pose_display_frame = tk.Frame(self.dataFrame, bg="white")
        self.pose_display_frame.pack(side=tk.TOP, padx=0, pady=10, fill=tk.BOTH)

        self.goto_vector_label = ttk.Label(self.pose_display_frame, text="Pose:", style="heading.TLabel", anchor="w", background="white")
        self.goto_vector_label.pack(pady=2, padx=0)


        self.pose_display_frame2 = tk.Frame(self.pose_display_frame, bg="white")
        self.pose_display_frame2.pack(side=tk.TOP, padx=0, pady=10, anchor="n")


        self.pose_display_entries = []
        for i in range(6):
            entry = ttk.Entry(self.pose_display_frame2, width=5, state="readonly")
            entry.grid(row=1, column=i, padx=1, pady=2)
            self.pose_display_entries.append(entry)


        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)

        self.ax1.set_title("Forces")
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Force (N)")

        self.ax2.set_title("Torques")
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Torque (Nm)")

        self.fig.tight_layout(pad=4.0)

        # Data shape: 2000 rows, 7 columns -> [ x, y1, y2, y3, y4, y5, y6 ]
        

        # Plot 1
        self.line1, = self.ax1.plot(self.data[:, 0], self.data[:, 1], label="Fx")
        self.line2, = self.ax1.plot(self.data[:, 0], self.data[:, 2], label="Fy")
        self.line3, = self.ax1.plot(self.data[:, 0], self.data[:, 3], label="Fz")

        self.ax1.legend()

        # Plot 2
        self.line4, = self.ax2.plot(self.data[:, 0], self.data[:, 4], label="Tx")
        self.line5, = self.ax2.plot(self.data[:, 0], self.data[:, 5], label="Ty")
        self.line6, = self.ax2.plot(self.data[:, 0], self.data[:, 6], label="Tz")

        self.ax2.legend()

        # Embed the figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.dataFrame)


        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.check_textbox()
        self.clearGraph()


    def importConfig(self):
        file_path = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json'), ('All files', '*.*')])
        if not file_path:
            return  # User canceled save
        self.loadConfigFile(file_path)



    def loadConfigFile(self, file):
        """Load a JSON configuration file into a dictionary and update UI elements."""
        try:
            with open(file, 'r') as f:
                self.config_data = json.load(f)

            # Update text entry for test name
            self.text_var.set(self.config_data.get("Test Name", ""))

            # Update start pose textboxes
            for i, value in enumerate(self.config_data.get("Start Pose", [0, 0, 0, 0, 0, 0])):
                self.start_pose_entries[i].delete(0, tk.END)
                self.start_pose_entries[i].insert(0, value)

            # Update retract vector textboxes
            for i, value in enumerate(self.config_data.get("Retract Vector", [0, 0, 0, 0, 0, 0])):
                self.retract_vector_entries[i].delete(0, tk.END)
                self.retract_vector_entries[i].insert(0, value)

            # Update test motion textboxes
            for i, value in enumerate(self.config_data.get("Test Vector", [0, 0, 0, 0, 0, 0])):
                self.test_motion_entries[i].delete(0, tk.END)
                self.test_motion_entries[i].insert(0, value)

            # Update align axis checkboxes
            for i, key in enumerate(["X", "Y", "Z", "U", "V", "W"]):
                self.align_vars[key].set(self.config_data.get("Align Axis", [1, 1, 1, 1, 1, 1])[i])

        except FileNotFoundError:
            print(f"Error: The file '{file}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file '{file}' contains invalid JSON.")
        except Exception as e:
            print(f"Unexpected error: {e}")



    def saveConfig(self, autosave):
        self.config_data["Test Name"] = self.test_name
        self.config_data["Start Pose"] = self.get_start_pose_values().tolist()
        self.config_data["Test Vector"] = self.get_test_vector_values().tolist()
        self.config_data["Retract Vector"] = self.get_retract_vector_values().tolist()
        self.config_data["Align Axis"] = self.get_checkbox_values().tolist()
        
        try:
            if autosave:
                with open("resources/TestConfigs/autosave.json", 'w') as f:
                    json.dump(self.config_data, f, indent=4)
            else:
                file = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('JSON Files', '*.json')], initialfile=self.test_name + ".json")
                if not file:
                    return  # User canceled save
                with open(file, 'w') as f:
                    json.dump(self.config_data, f, indent=4)
            
            
            print(f"Configuration saved to '{file}' successfully.")
        except Exception as e:
            print(f"Error saving configuration: {e}")



    def check_textbox(self, *args):
        """Enable buttons if text is entered in the text box."""
        self.setFileName()
        
    def setFileName(self):
        timestamp = datetime.now().strftime("_%m%d%y_%H%M")
        self.test_name = self.text_var.get()
        self.fileName = f"{self.test_name}{timestamp}.csv"
    
    def zeroRobotJoints(self):
        self.saveConfig(True)
        self.test.robot.moveToPos(np.zeros(6))
        self.updateGraph()

    def goToRetract(self):
        self.saveConfig(True)
        self.test.goToRetract( self.config_data["Start Pose"], self.config_data["Retract Vector"])
        self.updateGraph()

    def moveToStart(self):
        self.saveConfig(True)
        start_pose = np.array(self.get_start_pose_values())
        self.test.robot.moveToPos(start_pose)
        self.updateGraph()


    def align(self):
        self.testActive = False
        self.alignActive = True

        self.clearGraph()
        self.test.setAlignVector(self.get_checkbox_values())

        try:
            while self.alignActive:
                if(self.test.align()):
                    self.alignActive = False
                    self.getData()
                    self.updateGraph()
                self.root.update_idletasks()
                self.root.update()

        except tk.TclError:
            pass


    def start_test(self):
        self.testActive = True
        self.alignActive = False

        self.clearGraph()
        self.setFileName()
        self.saveConfig(True)

        self.test.setTestVector(self.get_test_vector_values())

        try:
            while self.testActive:
                if self.test.runTest():
                    self.testActive = False
                    self.getData()
                    self.updateGraph()
                self.root.update_idletasks()
                self.root.update()
                
        except tk.TclError:
            pass

    def getData(self):
        self.data[0:self.test.dataIndex-1, 0] = self.test.getXData()[0:self.test.dataIndex-1, 0]
        self.data[0:self.test.dataIndex-1, 1:7] = self.test.getWrencheData()[0:self.test.dataIndex-1, 0:6]
        # print(self.data[0:self.test.dataIndex])
        # print(self.test.getXData())


    def updateGraph(self):
        self.update_pose_display()
        x = self.data[:self.test.dataIndex-1, 0]
        # print(self.data)
        self.line1.set_xdata(x); self.line1.set_ydata(self.data[:self.test.dataIndex-1, 1])
        self.line2.set_xdata(x); self.line2.set_ydata(self.data[:self.test.dataIndex-1, 2])
        self.line3.set_xdata(x); self.line3.set_ydata(self.data[:self.test.dataIndex-1, 3])
        self.line4.set_xdata(x); self.line4.set_ydata(self.data[:self.test.dataIndex-1, 4])
        self.line5.set_xdata(x); self.line5.set_ydata(self.data[:self.test.dataIndex-1, 5])
        self.line6.set_xdata(x); self.line6.set_ydata(self.data[:self.test.dataIndex-1, 6])

        self.ax1.relim(); self.ax1.autoscale_view()
        self.ax2.relim(); self.ax2.autoscale_view()

        if self.testActive:
            if (np.any(self.get_test_vector_values()[3:6]) and not np.any(self.get_test_vector_values()[0:3])):
                self.ax1.set_xlabel("Angle (deg)")
                self.ax2.set_xlabel("Angle (deg)")
            else:
                self.ax1.set_xlabel("Distance (mm)")
                self.ax2.set_xlabel("Distance (mm)")

        self.canvas.draw()

    def clearGraph(self):
        self.data = np.zeros((2000, 7))
        self.test.clearData()
        self.updateGraph()

    def stop_test(self):
        self.testActive = False
        self.alignActive = False
        self.getData()
        self.updateGraph()
        # self.writeCSV()


    def get_checkbox_values(self):
        # Return the values in the order: X, Y, Z, U, V, W.
        return np.array([
            self.align_vars["X"].get(),
            self.align_vars["Y"].get(),
            self.align_vars["Z"].get(),
            self.align_vars["U"].get(),
            self.align_vars["V"].get(),
            self.align_vars["W"].get()
        ])


    def get_test_vector_values(self):
        """Return float values from the Test Motion text boxes as a numpy array."""
        values = []
        for entry in self.test_motion_entries:
            try:
                values.append(float(entry.get()))
            except ValueError:
                values.append(0.0)
        return np.array(values)

    def get_retract_vector_values(self):
        """Return float values from the Test Motion text boxes as a numpy array."""
        values = []
        for entry in self.retract_vector_entries:
            try:
                values.append(float(entry.get()))
            except ValueError:
                values.append(0.0)
        return np.array(values)


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


    def update_pose_display(self):
        """Update the uneditable text boxes with the current robot pose."""
        pose = self.test.robot.getPose()  # Expected to be a 1x6 numpy array
        for entry, val in zip(self.pose_display_entries, pose):
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, f"{val:.2f}")  # Format to 2 decimal places (adjust as needed)
            entry.config(state="readonly")

    def jogRobot(self, axis, direction):
        
        jog_vector = np.array([[1, 0, 0, 0, 0, 0],
                                [0, 1, 0, 0, 0, 0],
                                [0, 0, 1, 0, 0, 0],
                                [0, 0, 0, 1, 0, 0],
                                [0, 0, 0, 0, 1, 0],
                                [0, 0, 0, 0, 0, 1]])

        jog = np.array(direction * jog_vector[axis, :])
        self.jogActive = True
        
        while self.jogActive:
            self.test.jogRobot(jog)
            self.getData()
            self.updateGraph()
            # print("Jog")
            self.root.update_idletasks()
            self.root.update()


    def stopJog(self):
        self.jogActive = False

    def saveData(self):
        self.test.writeCSV(self.fileName)
    
    def resetError(self):
        print("TODO: RESET ROBOT ERROR")


def main():

    root = tk.Tk()
    SimpleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

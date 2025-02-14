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
        self.root.title("Tkinter + Matplotlib (While Loop)")

        style = ttk.Style()
        style.configure("Custom.TLabelframe.Label", font=("Helvetica", 12, "bold"))

        # Example "test" object for data collection
        self.test = Test()
        self.testActive = False
        self.alignActive = False

        self.fileName = ""
        self.test_name = ""

        self.data = np.zeros((1, 7))

        self.config_data = {
            "Test Name": "",
            "Start Pose": [0, 0, 0, 0, 0, 0],
            "Test Motion": [0, 0, 0, 0, 0, 0],
            "Align Axis": [1, 1, 1, 1, 1, 1]
        }

        self.loadConfigFile("resources/TestConfigs/autosave.json")
        
        
        # -------------------------------
        # 1) Frame: Text I/O + Buttons
        # -------------------------------
        frame = ttk.Frame(root, padding=5)
        frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(frame, text="Test Name:", font=("Helvetica", 12, "bold")).pack(side=tk.TOP)

        self.text_var = tk.StringVar()
        self.text_entry = ttk.Entry(frame, textvariable=self.text_var, width=15)
        self.text_entry.pack(side=tk.TOP, padx=5)
        self.text_entry.insert(0, self.config_data["Test Name"])
        self.text_var.trace_add("write", self.check_textbox)
        
    
        self.output_label = ttk.Label(frame, text="", background="white", width=20)
        self.output_label.pack(side=tk.TOP, padx=5)

        # -------------------------------
        # Container Frame for Two Sets of Buttons
        # -------------------------------
        buttons_container = ttk.Frame(frame)
        buttons_container.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        # Left set of buttons frame
        left_frame = ttk.Frame(buttons_container)
        left_frame.pack(side=tk.LEFT, padx=5)

        # Right set of buttons frame
        right_frame = ttk.Frame(buttons_container)
        right_frame.pack(side=tk.LEFT, padx=5)

        # Common button width for both sets
        button_width = 15

        # Left Set of Buttons

        tk.Label(left_frame, text="Test Commands").pack(side=tk.TOP)

        self.start_button = ttk.Button(left_frame, text="Start Test", command=self.start_test, state=tk.DISABLED, width=button_width)
        self.start_button.pack(side=tk.TOP, pady=2, fill=tk.X)

        self.clear_button = ttk.Button(left_frame, text="Clear Graph", command=self.clearGraph, state=tk.DISABLED, width=button_width)
        self.clear_button.pack(side=tk.TOP, pady=2, fill=tk.X)

        self.align_button = ttk.Button(left_frame, text="Align", command=self.align, state=tk.DISABLED, width=button_width)
        self.align_button.pack(side=tk.TOP, pady=2, fill=tk.X)

        self.stop_button = ttk.Button(left_frame, text="Stop Test", command=self.stop_test, state=tk.DISABLED, width=button_width)
        self.stop_button.pack(side=tk.TOP, pady=2, fill=tk.X)

        self.save_button = ttk.Button(left_frame, text="Save Test Data", command=self.saveData, width=button_width)
        self.save_button.pack(side=tk.TOP, pady=2, fill=tk.X)

        self.save_button = ttk.Button(left_frame, text="Save Test Config", command=partial(self.saveConfig, False), width=button_width)
        self.save_button.pack(side=tk.TOP, pady=2, fill=tk.X)

        self.save_button = ttk.Button(left_frame, text="Import Test Config", command=self.importConfig, width=button_width)
        self.save_button.pack(side=tk.TOP, pady=2, fill=tk.X)



        # Right Set of Buttons (Add your desired functionality)
        tk.Label(right_frame, text="Robot Commands").pack(side=tk.TOP)
        self.buttonA = ttk.Button(right_frame, text="Zero all joints", command=self.zeroRobotJoints, width=button_width)
        self.buttonA.pack(side=tk.TOP, pady=2, fill=tk.X)

        self.buttonB = ttk.Button(right_frame, text="Go to start pose", command=self.moveToStart, width=button_width)
        self.buttonB.pack(side=tk.TOP, pady=2, fill=tk.X)

        self.buttonC = ttk.Button(right_frame, text="Reset Error", command=self.resetError, width=button_width)
        self.buttonC.pack(side=tk.TOP, pady=2, fill=tk.X)
        

        # -------------------------------
        # Start Pose - Textboxes with Labels
        # -------------------------------
        self.start_pose_frame = ttk.LabelFrame(frame, text="Start Pose", padding=5, style="Custom.TLabelframe")
        self.start_pose_frame.pack(side=tk.TOP, padx=1, pady=1, fill=tk.X)

        # List of labels to display above the entries
        labels = ["x", "y", "z", "u", "v", "w"]
        self.start_pose_entries = []
        for i, label_text in enumerate(labels):
            lbl = ttk.Label(self.start_pose_frame, text=label_text)
            lbl.grid(row=0, column=i, padx=1, pady=2)
            entry = ttk.Entry(self.start_pose_frame, width=4)
            entry.grid(row=1, column=i, padx=1, pady=2)
            entry.insert(0, self.config_data["Start Pose"][i])
            self.start_pose_entries.append(entry)

        # -------------------------------
        # 3) Test Motion - Textboxes (Horizontally aligned)
        # -------------------------------

        self.test_motion_frame = ttk.LabelFrame(frame, text="Test Motion", padding=5, style="Custom.TLabelframe")
        self.test_motion_frame.pack(side=tk.TOP, padx=1, pady=1, fill=tk.X)

        # Define labels for each axis and create a single row of label-entry pairs.
        labels = ["X:", "Y:", "Z:", "U:", "V:", "W:"]
        self.test_motion_entries = []
        for i, label_text in enumerate(labels):
            lbl = ttk.Label(self.test_motion_frame, text=label_text)
            lbl.grid(row=0, column=i, padx=1, pady=2)
            entry = ttk.Entry(self.test_motion_frame, width=4)
            entry.grid(row=1, column=i, padx=1, pady=2)
            entry.insert(0, self.config_data["Test Motion"][i])
            self.test_motion_entries.append(entry)

        # -------------------------------
        # 4) Align Axis - Checkboxes (Horizontally aligned)
        # -------------------------------
        self.align_axis_frame = ttk.LabelFrame(frame, text="Align Axis", padding=5, style="Custom.TLabelframe")
        self.align_axis_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        # Create checkboxes for each axis in a single row.
        self.align_vars = {}  # We'll store the IntVars in a dictionary.
        for i, axis in enumerate(["X", "Y", "Z", "U", "V", "W"]):
            var = tk.IntVar(value=self.config_data["Align Axis"][i])
            chk = tk.Checkbutton(self.align_axis_frame, text=axis, variable=var)
            chk.grid(row=0, column=i, padx=5, pady=2)
            self.align_vars[axis] = var
        
        # -------------------------------
        # Axis Controls - Horizontal Layout
        # -------------------------------
        self.axis_controls_frame = ttk.LabelFrame(frame, text="Axis Controls", padding=5, style="Custom.TLabelframe")
        self.axis_controls_frame.pack(side=tk.TOP, padx=1, pady=10, fill=tk.X)

        axes = ["X", "Y", "Z", "U", "V", "W"]
        self.axis_buttons = {}

        # Row 0: Axis labels
        for i, axis in enumerate(axes):
            lbl = ttk.Label(self.axis_controls_frame, text=axis)
            lbl.grid(row=0, column=i, padx=1, pady=2)

        # Row 1: Plus buttons
        for i, axis in enumerate(axes):
            plus_button = ttk.Button(self.axis_controls_frame, text="+", width=1)
            plus_button.grid(row=1, column=i, padx=1, pady=2)
            plus_button.bind("<ButtonPress-1>", lambda event, idx=i: self.start_axis_move(idx, +1))
            plus_button.bind("<ButtonRelease-1>", lambda event: self.stop_axis_move())
            self.axis_buttons[axis] = {"plus": plus_button}

        # Row 2: Minus buttons
        for i, axis in enumerate(axes):
            minus_button = ttk.Button(self.axis_controls_frame, text="-", width=1)
            minus_button.grid(row=2, column=i, padx=1, pady=2)
            minus_button.bind("<ButtonPress-1>", lambda event, idx=i: self.start_axis_move(idx, -1))
            minus_button.bind("<ButtonRelease-1>", lambda event: self.stop_axis_move())
            self.axis_buttons[axes[i]]["minus"] = minus_button

        # -------------------------------
        # Current Pose Display - Uneditable text boxes
        # -------------------------------
        self.pose_display_frame = ttk.LabelFrame(frame, text="Current Pose", padding=5, style="Custom.TLabelframe")
        self.pose_display_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        labels = ["x", "y", "z", "u", "v", "w"]
        self.pose_display_entries = []
        for i, label_text in enumerate(labels):
            lbl = ttk.Label(self.pose_display_frame, text=label_text)
            lbl.grid(row=0, column=i, padx=1, pady=2)
            entry = ttk.Entry(self.pose_display_frame, width=4, state="readonly")
            entry.grid(row=1, column=i, padx=1, pady=2)
            self.pose_display_entries.append(entry)

            
        # -------------------------------
        # 2) Figure and initial plots
        # -------------------------------
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
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.check_textbox()


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

            # Update test motion textboxes
            for i, value in enumerate(self.config_data.get("Test Motion", [0, 0, 0, 0, 0, 0])):
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


    # def loadConfigFile(self, file):
    #     """Load a JSON configuration file into a dictionary."""
    #     try:
    #         with open(file, 'r') as f:
    #             self.config_data = json.load(f)
    #     except FileNotFoundError:
    #         print(f"Error: The file '{file}' was not found.")
    #     except json.JSONDecodeError:
    #         print(f"Error: The file '{file}' contains invalid JSON.")
    #     except Exception as e:
    #         print(f"Unexpected error: {e}")



    def saveConfig(self, autosave):
        self.config_data["Test Name"] = self.test_name
        self.config_data["Start Pose"] = self.get_start_pose_values().tolist()
        self.config_data["Test Motion"] = self.get_test_vector_values().tolist()
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
        if self.text_var.get():
            self.start_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL)
            self.align_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.DISABLED)
            self.align_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)
        self.setFileName()
        
    def setFileName(self):
        timestamp = datetime.now().strftime("_%m%d%y_%H%M")
        self.test_name = self.text_var.get()
        self.fileName = f"{self.test_name}{timestamp}.csv"
        self.output_label.config(text=self.fileName)
    
    def zeroRobotJoints(self):
        self.test.robot.moveToPos(np.zeros(6))
        self.updateGraph()

    def moveToStart(self):
        start_pose = np.array(self.get_start_pose_values())
        self.test.robot.moveToPos(start_pose)
        self.updateGraph()


    def align(self):
        self.testActive = False
        self.alignActive = True
        self.output_label.config(text="Aligning")

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
        self.data = np.zeros((self.test.dataIndex, 7))
        self.data[:, 0] = self.test.getXData()[:, 0]
        self.data[:, 1:7] = self.test.getWrencheData()[:, 0:6]
        # print(self.data)


    def updateGraph(self):
        self.update_pose_display()
        x = self.data[:, 0]
        print(self.data)
        self.line1.set_xdata(x); self.line1.set_ydata(self.data[:, 1])
        self.line2.set_xdata(x); self.line2.set_ydata(self.data[:, 2])
        self.line3.set_xdata(x); self.line3.set_ydata(self.data[:, 3])
        self.line4.set_xdata(x); self.line4.set_ydata(self.data[:, 4])
        self.line5.set_xdata(x); self.line5.set_ydata(self.data[:, 5])
        self.line6.set_xdata(x); self.line6.set_ydata(self.data[:, 6])

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
        self.data = np.zeros((1, 7))
        self.test.clearData()
        self.updateGraph()

    def stop_test(self):
        self.testActive = False
        self.alignActive = False
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

import os
import sys

from matplotlib.pylab import f

sys.path.append(os.path.join(os.path.dirname(__file__), "resources"))
sys.path.append(os.path.join(os.path.dirname(__file__), "resources/UI_Pages"))

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



from datetime import datetime

import json

from page_test_setup import SetupTestPage  # Import MotionPage
from page_run_test import RunTestPage  # Import MotionPage
from style import get_ui_style # Import the style function defined in style.py 



class SimpleApp:
    def __init__(self, root):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(base_dir)
    
        self.root = root
        self.root.title("Noodle Test")
        self.root.resizable(False, False)  # or root.resizable(0, 0)
        
        ui_style = get_ui_style()
        self.style = ui_style["style"]
        # Assign UI dimension variables
        self.padding = ui_style["padding"]
        self.textbox_width = ui_style["textbox_width"]
        self.button_width = ui_style["button_width"]
        self.button_width2 = ui_style["button_width2"]
        self.component_width = ui_style["component_width"]
        

        # Example "test" object for data collection
        self.test = Test()
        self.testActive = False
        self.alignActive = False
        self.jogActive = False

        self.fileName = ""
        self.test_name = ""

        self.data = np.zeros((2000, 7))

        self.config_data = {
            "Robot IP": "192.169.0.100",
            "Sensor Port": "en13",
            "Test Name": "",
            "Start Pose": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Retract Vector": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Test Vector": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Align Axis": [1, 1, 1, 1, 1, 1]
        }

        self.loadConfigFile("resources/TestConfigs/autosave.json")
        

        # -------------------------------
        # 1) Frame: LEFT
        # -------------------------------
        leftframe = tk.Frame(root, background="#ebebeb")
        leftframe.pack(side=tk.LEFT, padx=0, pady=2, fill=tk.Y)

        # -------------------------------
        # 1) Frame: LEFT Menu
        # -------------------------------

        menu_frame = tk.Frame(leftframe, bg="gray")
        menu_frame.pack(side=tk.TOP, padx=0, pady=0, fill=tk.X)

        # Create buttons for each page
        self.settings_button = ttk.Button(menu_frame, text="Setup", command=lambda: self.show_page("Setup"), style="secondary.TButton", width=self.button_width)
        self.settings_button.pack(side=tk.LEFT, padx=0, pady=0)

        self.test_button = ttk.Button(menu_frame, text="Test", command=lambda: self.show_page("Run"), style="secondary.TButton", width=self.button_width)
        self.test_button.pack(side=tk.LEFT, padx=0, pady=0)

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
       

        self.padFrame = tk.Frame(frame)
        self.padFrame.pack(pady=20, padx=0)


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
        


        self.test_setup_page = SetupTestPage(frame, self, self.config_data)
        self.run_test_page = RunTestPage(frame, self, self.config_data)

        self.menu_pages = {
            "Setup": self.test_setup_page,
            "Run": self.run_test_page
        }

        self.check_textbox()
        self.clearGraph()

        # Show the initial page
        self.show_page("Setup")


    def show_page(self, page_name):
            """Swap the left-side content with the selected page."""
            for page in self.menu_pages.values():
                page.pack_forget()  # Hide all pages
            self.menu_pages[page_name].pack(fill="both", expand=True)  # Show selected page


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
        self.config_data["robotIP"] = self.config_data["Robot IP"]
        self.config_data["sensorPort"] = self.config_data["Sensor Port"]
        self.config_data["Test Name"] = self.test_name
        self.config_data["Start Pose"] = self.test_setup_page.get_start_pose_values().tolist()
        self.config_data["Test Vector"] = self.test_setup_page.get_test_vector_values().tolist()
        self.config_data["Retract Vector"] = self.test_setup_page.get_retract_vector_values().tolist()
        self.config_data["Align Axis"] = self.run_test_page.get_checkbox_values().tolist()
        
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
            if (np.any(self.config_data["Start Pose"][3:6]) and not np.any(self.config_data["Start Pose"][0:3])):
                self.ax1.set_xlabel("Angle (deg)")
                self.ax2.set_xlabel("Angle (deg)")
            else:
                self.ax1.set_xlabel("Distance (mm)")
                self.ax2.set_xlabel("Distance (mm)")
        else:
            self.ax1.set_xlabel("Time (ms)")
            self.ax2.set_xlabel("Time (ms)")

        self.canvas.draw()

    def clearGraph(self):
        self.data = np.zeros((2000, 7))
        self.test.clearData()
        self.updateGraph()


    def update_pose_display(self):
        """Update the uneditable text boxes with the current robot pose."""
        pose = self.test.robot.getPose()  # Expected to be a 1x6 numpy array
        for entry, val in zip(self.pose_display_entries, pose):
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, f"{val:.2f}")  # Format to 2 decimal places (adjust as needed)
            entry.config(state="readonly")

   
def main():

    root = tk.Tk()
    SimpleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

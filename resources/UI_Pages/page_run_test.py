import tkinter as tk
from tkinter import ttk


from style import get_ui_style

import numpy as np


class RunTestPage(tk.Frame):
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


        self.padFrame = tk.Frame(self)
        self.padFrame.pack(pady=15, padx=0)

        self.goto_vector_label = ttk.Label(self, text="Go To:", style="heading.TLabel", anchor="w")
        self.goto_vector_label.pack(pady=2, padx=0, anchor="w")

        config_goto_container = tk.Frame(self)
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

        self.test_button = ttk.Button(self, text="Reset Errors", command=self.moveToStart, style="primary.TButton", width=int(self.textbox_width -3))
        self.test_button.pack(side=tk.TOP, pady=2, padx=self.padding, fill=tk.X)

       
        # -------------------------------
        # 4) Align Axis 
        # -------------------------------

        self.padFrame = tk.Frame(self)
        self.padFrame.pack(pady=15, padx=0)
        
        self.goto_vector_label = ttk.Label(self, text="Align:", style="heading.TLabel", anchor="w")
        self.goto_vector_label.pack(pady=2, padx=0, anchor="w")

        self.align_axis_frame = tk.Frame(self)
        self.align_axis_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        # Create checkboxes for each axis in a single row.
        self.align_vars = {}  # We'll store the IntVars in a dictionary.
        for i, axis in enumerate(["X", "Y", "Z", "U", "V", "W"]):
            var = tk.IntVar(value=self.config_data["Align Axis"][i])
            self.align_vars[axis] = var
            chk = tk.Checkbutton(self.align_axis_frame, text=axis, variable=var)
            chk.grid(row=0, column=i, padx=6, pady=2)

        self.align_button = ttk.Button(self, text="Align", command=self.align, style="primary.TButton", width=int(self.textbox_width -3))
        self.align_button.pack(side=tk.TOP, pady=1, fill=tk.X)
            
            
        # -------------------------------
        # Axis Controls
        # -------------------------------

        self.padFrame = tk.Frame(self)
        self.padFrame.pack(pady=5, padx=0)

        self.axis_controls_frame = tk.Frame(self)
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
        
        self.padFrame = tk.Frame(self)
        self.padFrame.pack(pady=20, padx=0)

        test_buttons_container = tk.Frame(self)
        test_buttons_container.pack(side=tk.BOTTOM, padx=0, pady=2, fill=tk.Y)

        # Create sub-frames for left and right
        start_test_frame = tk.Frame(test_buttons_container)
        start_test_frame.grid(row=0, column=0, padx=0, pady=2, sticky="ew")  # Use grid and fill horizontally

        save_data_frame = tk.Frame(test_buttons_container)
        save_data_frame.grid(row=0, column=1, padx=0, pady=2, sticky="ew")  # Same here, align horizontally


        self.clear_button = ttk.Button(start_test_frame, text="Clear Graph", style="secondary.TButton", command=self.clearGraph,width=self.button_width)
        self.clear_button.pack(side=tk.TOP, pady=2, padx=self.padding, fill=tk.X)

        self.save_button = ttk.Button(save_data_frame, text="Save Test Data", command=self.saveData, style="secondary.TButton", width=self.button_width)
        self.save_button.pack(side=tk.TOP, pady=2, padx=self.padding,fill=tk.X)


        self.start_button = ttk.Button(self, text="Start Test", command=self.start_test, style="start.TButton", width=int(self.textbox_width -3))
        self.start_button.pack(side=tk.TOP, pady=2, padx=self.padding, fill=tk.X)

        self.stop_button = ttk.Button(self, text="Stop Test", command=self.stop_test, style="primary.TButton", width=int(self.textbox_width -3))
        self.stop_button.pack(side=tk.TOP, pady=2, padx=self.padding, fill=tk.X)



    def zeroRobotJoints(self):
        self.controller.test.robot.moveToPos(np.zeros(6))
        self.controller.updateGraph()

    def goToRetract(self):
        self.controller.saveConfig(True)
        self.controller.test.goToRetract(self.config_data["Start Pose"], self.config_data["Retract Vector"])
        self.controller.updateGraph()

    def moveToStart(self):
        self.controller.saveConfig(True)
        start_pose = self.config_data["Start Pose"]
        self.controller.test.robot.moveToPos(start_pose)
        self.controller.updateGraph()


    def align(self):
        self.controller.testActive = False
        self.controller.alignActive = True

        self.controller.clearGraph()
        self.controller.test.setAlignVector(self.get_checkbox_values())

        try:
            while self.controller.alignActive:
                if(self.controller.test.align()):
                    print("Align")
                    self.controller.getData()
                    self.controller.updateGraph()
                    self.controller.alignActive = False
                self.root.update_idletasks()
                self.root.update()

        except tk.TclError:
            pass


    def start_test(self):
        self.controller.testActive = True
        self.controller.alignActive = False

        self.controller.clearGraph()
        self.controller.setFileName()
        self.controller.saveConfig(True)

        self.controller.test.setTestVector(self.config_data["Test Vector"])

        try:
            while self.controller.testActive:
                if self.controller.test.runTest():
                    self.controller.getData()
                    self.controller.updateGraph()
                    self.controller.testActive = False
                self.root.update_idletasks()
                self.root.update()
                
        except tk.TclError:
            pass

    def stop_test(self):
        self.controller.getData()
        self.controller.updateGraph()
        self.controller.testActive = False
        self.controller.alignActive = False
        
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

    def jogRobot(self, axis, direction):
        
        jog_vector = np.array([[1, 0, 0, 0, 0, 0],
                                [0, 1, 0, 0, 0, 0],
                                [0, 0, 1, 0, 0, 0],
                                [0, 0, 0, 1, 0, 0],
                                [0, 0, 0, 0, 1, 0],
                                [0, 0, 0, 0, 0, 1]])

        jog = np.array(direction * jog_vector[axis, :])
        self.controller.jogActive = True
        
        while self.controller.jogActive:
            self.controller.test.jogRobot(jog)
            self.controller.getData()
            self.controller.updateGraph()
            # print("Jog")
            self.root.update_idletasks()
            self.root.update()

    def stopJog(self):
        self.controller.jogActive = False

    def saveData(self):
        self.controller.test.writeCSV(self.controller.fileName)
    
    def resetError(self):
        print("TODO: RESET ROBOT ERROR")


    def clearGraph(self):
        self.controller.clearGraph()


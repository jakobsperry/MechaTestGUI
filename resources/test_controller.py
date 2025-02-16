from robot import Robot
from tkinter import filedialog
import math
import numpy as np
import time
import csv

class Test:

    def __init__ (self):
        self.robot = Robot()
        
        self.empty_array = np.zeros((2000, 6))
        self.empty_x_array = np.zeros((2000, 1))
        
        self.wrench_Data = self.empty_array.copy()
        self.pose_data = self.empty_array.copy()
        self.x_data = self.empty_x_array.copy()
        self.time_data = self.empty_x_array.copy()
        self.sampleTime_data = self.empty_x_array.copy()

        
        self.test_vector = np.zeros([6])
        self.align_vector = np.zeros([6])

        self.start_time = time.time()
        self.curr_time = time.time()
        self.last_time = time.time()
        self.dataIndex = 0


        self.start_pose = np.zeros(6)

        self.start_target = np.zeros(6)

        self.curr_pose = np.zeros(6)

        self.time_interval = 60

        self.setup_test = True

        self.speed = 0.5


    def updateData(self, xValue, sample_time):
        # print(xValue)
        self.x_data[self.dataIndex] = xValue
        self.sampleTime_data[self.dataIndex] = sample_time
        self.time_data[self.dataIndex] = self.getRuntime()
        self.pose_data[self.dataIndex] = self.robot.getPose()
        self.wrench_data[self.dataIndex] = self.robot.getWrench()

    def getPoseData(self):
        return self.pose_data[0:(self.dataIndex), :]

    def getWrencheData(self):
        return self.wrench_data[0:(self.dataIndex), :]

    def getXData(self):
        return self.x_data[0:(self.dataIndex)]


    def getRuntime(self):
        curr_time = time.time()
        runtime_ms = (curr_time - self.start_time) * 1000
        return runtime_ms
    

    def setTestVector(self, vector):
        self.test_vector = vector
    
    def setAlignVector(self, vector):
        self.align_vector = vector

    def calculateDistance(self):
        if np.any(self.test_vector[3:6]):
            distance = np.linalg.norm(self.robot.getPose()[3:6] - self.start_pose[3:6])
        else:
            distance = np.linalg.norm(self.robot.getPose()[0:3] - self.start_pose[0:3])
        if math.isnan(distance):
            return 0.0
        return distance


    def runTest(self):
        if self.setup_test:
            self.start_pose = self.robot.getPose()
            self.setup_test = False
            # print(self.start_pose)
        
        self.curr_time = time.time()
        sample_time = (self.curr_time - self.last_time) * 1000
        if (sample_time > self.time_interval):
            self.last_time = self.curr_time
            distance = self.calculateDistance()
            
            max = np.max(np.abs(self.test_vector))
            vel_vector = self.test_vector/max * self.speed

            self.robot.moveLinVel(vel_vector, self.getRuntime())
            # print(distance)
            direction = np.sign(self.test_vector)
            curr_pose = self.robot.getPose()
            if np.any((direction > 0) & (curr_pose > (self.start_pose + self.test_vector))) | np.any((direction < 0) & (curr_pose < (self.start_pose + self.test_vector))) or np.all(self.test_vector == 0):
                self.setup_test = True
                return True
            self.updateData(distance, sample_time)
            self.dataIndex += 1
            

    def goToRetract(self, startPose, retract):
        self.robot.pose = np.array(np.array(startPose) + np.array(retract))


    def align(self):
        self.curr_time = time.time()
        sample_time = (self.curr_time - self.last_time) * 1000
        if (sample_time > self.time_interval):
            self.last_time = self.curr_time
            runtime = self.getRuntime()
            self.robot.align(runtime, self.align_vector)
            self.updateData(runtime, sample_time)
            self.dataIndex += 1

            if(np.all((self.robot.getWrench()*self.align_vector) < 0.005)):
                return True

    def clearData(self):
        self.dataIndex = 0
        self.wrench_data = self.empty_array.copy()
        self.pose_data = self.empty_array.copy()
        self.time_data = self.empty_x_array.copy()
        self.x_data = self.empty_x_array.copy()
        self.sampleTime_data = self.empty_x_array.copy()

    def jogRobot(self, vector):
        self.curr_time = time.time()
        sample_time = (self.curr_time - self.last_time) * 1000
        if (sample_time > self.time_interval):
            self.last_time = self.curr_time
            runtime = self.getRuntime()
            self.robot.moveLinVel(vector, self.getRuntime())
            self.updateData(runtime, sample_time)
            self.dataIndex += 1


    def writeCSV(self, fileName):
        header = np.array(["time (ms)", "Sample time (ms)", "Calculated X Axis (mm, deg or ms)", "X (mm)", "Y (mm)", "Z (mm)", "U (deg)", "V (deg)", "W (deg)", "Fx (N)", "Fy (N)", "Fz (N)", "Tx (Nm)", "Fy (Nm)", "Tz (Nm)"])
        csv_filename = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')], initialfile=fileName)
        if not csv_filename:
            return  # User canceled save


        with open(csv_filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(np.concatenate((self.time_data, self.sampleTime_data, self.x_data, self.pose_data, self.wrench_data), axis=1)[0:self.dataIndex, :])

        

   
import numpy as np
import time

class Robot:

    def __init__(self):
        self.wrench = np.random.rand(6)
        self.pose = np.zeros(6)
        self.run_time = time.time()


    def getWrench(self):
        return np.array(self.wrench)
    
    def getPose(self):
        pose = np.array(self.pose)
        # print(pose)
        return pose

    def moveToPos(self, pose):
        self.pose = pose
        self.getPose()

    def moveLinVel(self, vector, runtime):
        self.pose += vector
        self.generateWrench(runtime)
        
    def generateWrench(self, runtime):
        fx  = np.sin(runtime/1000)
        fy  = np.cos(runtime/1000)
        fz  = 1.5 * np.sin(runtime/1500)

        tx  = np.sin(runtime/1000) / 2
        ty  = np.sin(runtime / 1500) / 2
        tz  = np.cos(runtime /2000) / 2

        self.wrench = (np.array([fx, fy, fz, tx, ty, tz]))

        return np.array([runtime, fx, fy, fz, tx, ty, tz])


    def align(self, runtime, align_vector):
        kp = 0.05
        self.wrench -= self.wrench * kp * align_vector
        self.pose -= self.wrench * kp * align_vector









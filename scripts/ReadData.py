#!/usr/bin/env python3

import numpy as np
import time
import rospy
from main_pkg.msg import SensorsData

class SensorController:
    def __init__(self):
        rospy.init_node('sensorscnt', anonymous=False)

        self.Pub = rospy.Publisher('/sensorsdata', SensorsData, queue_size=10)
        
        rate = rospy.get_param("~rate", 3000)
        self.filename = rospy.get_param("~filename", "dataset.npy")
        try:
            self._data = np.load(self.filename)
            self._dim = self._data.shape
            rospy.loginfo(f"Data loaded from {self.filename}")
        except Exception as e:
            rospy.logerr(f"Error loading data from {self.filename}: {e}")
        self._data = np.asarray(self._data)
        self.n_sensors = rospy.get_param("~n_sensors", 8)
        if self.n_sensors != self._dim[1]:
            # Put the channels in columns
            self._data = self._data.T
            self._dim = self._data.shape
        rospy.loginfo(f"Number of sensors: {self.n_sensors}")

        self.data = [0 for i in range(self.n_sensors)]
        self.rate = rospy.Rate(rate)


    def publish_data(self):
        msg = SensorsData()
        msg.data = self.data
        msg.timestamp = rospy.Time.now()
        self.Pub.publish(msg)
        self.rate.sleep()

    def read(self):
        data = list(self._data[self.counter % self._dim[0], :])
        return data

    def run(self):
        self.counter = -1
        while not rospy.is_shutdown():
            self.counter += 1
            data = self.read()
            self.data = data
            self.publish_data()
                      

if __name__ == '__main__':
    sensor_controller = SensorController()
    sensor_controller.run()
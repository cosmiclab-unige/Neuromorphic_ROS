#!/usr/bin/env python3

import rospy
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from collections import deque
from main_pkg.msg import SensorsData


class PlotterNode:
    def __init__(self):
        rospy.init_node('plotter_node', anonymous=True)

        # Parametri
        self.buffer_size = rospy.get_param("~buffer_size", 1000)
        self.n_sensors = rospy.get_param("~n_sensors", 8)
        self.data_buffer = [deque([0]*self.buffer_size, maxlen=self.buffer_size) for _ in range(self.n_sensors)]


        # Setup figura
        self.fig, self.ax = plt.subplots()
        self.lines = [self.ax.plot([], [], label=f"Sensor {i+1}")[0] for i in range(self.n_sensors)]

        self.ax.set_xlim(0, self.buffer_size)
        self.ax.set_ylim(0, 1)  # Adatta in base ai dati attesi
        self.ax.set_xlabel("Campioni")
        self.ax.set_ylabel("Valore Sensore")
        self.ax.set_title(f"Spikes (Last {self.buffer_size} Samples)")
        self.ax.legend()

        # Subscriber ROS
        rospy.Subscriber('/sensorsdata', SensorsData, self.callback)


    def callback(self, msg):
        data = msg.data
        if len(data) != self.n_sensors:
            rospy.logwarn("Numero di sensori ricevuti non corrisponde!")
            return
        for i in range(self.n_sensors):
            self.data_buffer[i].append(data[i])

    def run(self):
        rate = rospy.Rate(100)  # Frequenza di aggiornamento
        while not rospy.is_shutdown():
            for i in range(self.n_sensors):
                self.lines[i].set_xdata(range(self.buffer_size))
                self.lines[i].set_ydata(list(self.data_buffer[i]))
            plt.pause(0.01)  # Aggiorna il grafico
            rate.sleep()

if __name__ == '__main__':
    plotter = PlotterNode()
    plotter.run()

        

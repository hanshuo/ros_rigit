#!/usr/bin/env python
import roslib; roslib.load_manifest('ros_rigit')
import rospy
from ros_flydra.msg import *
from ros_rigit.msg import pose_object
from ros_rigit import rigit.rigit_nn as rigit_nn

import numpy
from numpy import *

class Listener:
    def __init__(self, max_freq):
        self.is_initialized = False
        self.max_freq = max_freq

        self.pub = rospy.Publisher('pose_estimation', pose_object)
        
        rospy.Subscriber('flydra_mainbrain_super_packets',
                         flydra_mainbrain_super_packet,
                         self.callback)
        
        rospy.init_node('rigit_from_flydra', anonymous=True)

    def callback(self, super_packet):
        packet = super_packet.packets[0] # super_packet legacy
        nobjs = len(packet.objects)
        self.world_pts = array([[obj.position.x, obj.position.y, obj.position.z]
                                for obj in packet.objects]).T

        if not self.is_initialized:
            self.world_pts_init = self.world_pts
            self.is_initialized = True
            
    def run(self):
        loop_rate = rospy.Rate(self.max_freq)
        
        while not rospy.is_shutdown():
            if self.is_initialized:
                R, T, err = rigit_nn(self.world_pts_init, self.world_pts)
                self.pub.publish(R.flatten().tolist(), T.tolist())

            loop_rate.sleep()

if __name__ == '__main__':
    max_freq = 20              # Running at 20 Hz maximum

    listener = Listener(max_freq)
    listener.run()


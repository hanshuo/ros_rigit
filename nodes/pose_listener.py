#!/usr/bin/env python
import roslib; roslib.load_manifest('ros_rigit')
import rospy
from ros_rigit.msg import pose_object

import numpy
from numpy import *

class Listener:
    def __init__(self):
        rospy.Subscriber('pose_estimation', pose_object, self.callback)
        rospy.init_node('pose_listener', anonymous=True)
        rospy.spin()
        
    def callback(self, pose_packet):
        print '-'*80
        print 'R = '
        print array(pose_packet.R).reshape(3,3)
        print 'T = '
        print array(pose_packet.T)

if __name__ == '__main__':
    listener = Listener()


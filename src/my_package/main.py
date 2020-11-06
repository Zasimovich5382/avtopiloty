#! /usr/bin/python

import rospy
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist
from numpy import pi 
from math import atan2


class Main():
	def __init__(self):
		self.rPose = Pose()
		self.fPose = Pose()
		self.rabb_sub = rospy.Subscriber('/michelangelo/pose', Pose, self.set_pose_outsider)
		self.runner_sub = rospy.Subscriber('/raphael/pose', Pose, self.set_pose_favorite)
		self.runner_pub = rospy.Publisher('/raphael/cmd_vel', Twist, queue_size = 1)


	def run(self):
		while not rospy.is_shutdown():
			ang = atan2(self.rPose.y - self.fPose.y, self.rPose.x - self.fPose.x) - self.fPose.theta
			msg = Twist()
			msg.angular.z = ang
			msg.linear.x = (pi - abs(ang)) / pi
			self.runner_pub.publish(msg)

					
	def set_pose_outsider(self, pose):
		self.rPose = pose


	def set_pose_favorite(self, pose):
		self.fPose = pose
		
rospy.init_node('race')
rospy.wait_for_service('/spawn')
spawn_func = rospy.ServiceProxy('/spawn', Spawn)
res = spawn_func(0.0, 6.0, 3.0, 'raphael')
m = Main()
m.run()

#! /usr/bin/env python3

"""

.. module:: node_c
   :platform: Unix
   :synopsys: Documentation fro Node "C" from assignment 02 of RT1
	
..moduleauthor:: Aicha Manar ABBAD

Node 'c' is used to compute the distance between the robot position and its final taget. Also used to compute the robot average velocity.

Subscribes to :
	/position_and_velocity
	/reaching_goal/result

"""

import rospy
import assignment_2_2022.msg
import math
import nav_msgs.msg
import actionlib

from assignment_2_2022.msg import position

""" Declaring global variables
"""
distance =  0.0
begin_time = 0.0
end_time = 0.0
velocity = 0.0



def sub_callback(data):
	
	"""
	
	*sub_callback()* is a callback function used for subsription to *"position_and_velocity"*.
	It declared the global varialbles (*end_time*, *begin_time*, *distance*, and *velocity*) and 
	call the *compute_distance()* function.
	
	"""
	global end_time, begin_time, distance, velocity
	compute_distance(data)


def sub2_callback(data):

	"""
	
	*sub2_callback()* is a callback function used for subsription to *"/reaching_goal/result"*.
	It declared the global varialbles (*end_time*, *begin_time*, *distance*, and *velocity*) and 
	call the *compute_velocity()* function. After that it returns the *distance* to the goal and 
	the average *velocity* of the robot.
	
	"""

	global end_time, begin_time, distance, velocity
	compute_velocity(data) 
	print(f"The distance to the goal is {distance} \nThe average speed of the robot is {velocity}")
	

## Function to compute the distance between the current
# position of the robot and goal position
def compute_distance(data):
	
	"""
	
	*compute_distance()* is a function used to compute the distance to the target.
	
	"""
	
	global begin_time, distance
	""" get the desired 'x' and 'y' positions using *rospy.get_param()*.
	"""
	x_pos = rospy.get_param("/des_pos_x")
	y_pos = rospy.get_param("/des_pos_y")

	""" get the current position of the robot from *data.x_pos* and *data.y_pos*. And set the *begin_time* to the current time.
	"""
	x = data.x_pos
	y = data.y_pos
	begin_time = rospy.Time.now()
	
	"""compute the distance to the goal using *distance = math.sqrt((x_dist**2) + (y_dist**2))* while *x_dist* and *y_dist* is equale
	to the distance between the initial and the target position of the robot.
	"""
	x_dist = x_pos - x
	y_dist = y_pos - y
	distance = math.sqrt((x_dist**2) + (y_dist**2))
	
	

## The function to compute the average velocity of the robot
def compute_velocity(data):
	
	"""
	
	*compute_velocity()* is a function used to compute the average velocity of the robot.
	
	"""
	
	global end_time, begin_time, distance, velocity
	if (data.status.status == 3): 
		""" when the robot reaches the goal.
		"""
		end_time = rospy.Time.now() 
		""" get the time at the moment the robot reaches the target.
		"""

		time = (end_time - begin_time).to_sec()
		""" compute the average time *end_time - begin_time*
		"""
		velocity = distance/time 
		""" compute the velocity *velocity = distance/time *
		"""


if __name__ == "__main__":
	rospy.init_node("node_c") 
	""" initialize the node
	"""
	rospy.Subscriber("position_and_velocity", position,sub_callback)
	""" Subscribes *position_and_velocity*
	"""
	rospy.Subscriber('/reaching_goal/result', assignment_2_2022.msg.PlanningActionResult, sub2_callback)
	""" Subscribes */reaching_goal/result*
	"""
	rospy.spin()



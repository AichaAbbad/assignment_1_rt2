#! /usr/bin/env python3

"""

.. module:: node_a
   :platform: Unix
   :synopsys: Documentation fro Node "A" from assignment 02 of RT1
	
..moduleauthor:: Aicha Manar ABBAD

Node 'a' implements an action client that allows the user to set a goal or cancel it.
It also publishes the velocity as a costum message based on the values published in
the '/odom' topic.

Subscribes to :
	/odom

Publishes to :
	/position_and_velocity
	
ActionClient to :
	/reaching_goal
	
"""

import rospy
import actionlib
import geometry_msgs.msg
import assignment_2_2022.msg
import nav_msgs.msg

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from assignment_2_2022.msg import position


"""Define functions"""

def sub_callback(data):

	"""
	
	*sub_callback()* is a callback function. It gets the current 
	odometry data from *"/odom"* and publish it using costum messages
	in *"/position_and_velocity"*.

	"""
	
	costum_msg = position()
	costum_msg.x_pos = data.pose.pose.position.x 
	""" get the current x position 
	"""
	costum_msg.y_pos = data.pose.pose.position.y 
	""" get the current y position
	"""
	costum_msg.x_velocity_val = data.twist.twist.linear.x 
	""" get the current x velocity value 
	"""
	costum_msg.y_velocity_val = data.twist.twist.linear.y 
	""" get the current y velocity value 
	"""
	rospy.loginfo(rospy.get_caller_id() + " Odometry data received !\n %s",data)	
	publish_msg(costum_msg) 
	""" Call function to publish the data 
	"""

	

def publish_msg(costum_msg):
	
	"""
	
	*publish_msg()* is a function for publishing odometry data.
	It publishes the current odometry data in in *"/position_and_velocity"*
	
	"""	

	publisher = rospy.Publisher("position_and_velocity",position,queue_size = 10)
	""" Publish the data on costum_msg
	"""
	publisher.publish(costum_msg)
	print("Message published !")
	main()



def set_target():

	"""
	
	*set_target()* is a function used to ask the user to inter the target goal.
	This function allows the user to inter the desired goal it wants to reach
	and send it to the client server.
	
	"""

	x = float(input("Enter the value os the x position: "))
	""" Input *"x"* value
	"""
	y = float(input("Enter the value os the Y position: "))	
	""" Input *"x"* value
	"""
	print(f'Position entered sucessefully: \n x position: {x} \n y position: {y}')	
	client.wait_for_server()
	""" wait for the server
	"""	
	goal = PoseStamped()	
	goal.pose.position.x = x
	goal.pose.position.y = y
	goal = assignment_2_2022.msg.PlanningGoal(goal)		
	client.send_goal(goal) 
	""" send the goal to the action server
	"""
	

def cancel_target():

	"""
	
	*cancel_target()* is a function used to cancel the target set by the user.
	
	"""

	client.cancel_goal()
	print("Goal canceled !\n")
	main()



def wrong_target():
	
	"""
	
	*wrong_target()* is a function used to inform the user in case he inputs
	a wrong target.
	
	"""	
	
	print("The input is wrong, repeat again !\n")
	main()
	""" call the *main()* function
	"""


def main():

	"""
	
	*main()* is the main function of the program. It serves as a user interface
	where the client can choose one of the three options : 
		*1. Target :* to input the desired target.
		*2. Cancel :* to cancel the target.
		*3. Exit :* to exit the program
		
	"""	
	
	print("## Robot Control ##\n")
	print("1. Target\n")
	print("2. Cancel\n")
	print("3. Exit\n")	
	option = input("Select your option !\n")		
	if (option == "1"):
		print("\nsetting target ...\n")
		set_target()
		print("\nset target!\n")
	elif (option == "2"):
		cancel_target()
	elif (option =="3"):
		exit()
	else:
		wrong_target()

if __name__ == "__main__":
	rospy.init_node("node_a") 
	""" initialize the node
	"""
	client = actionlib.SimpleActionClient('/reaching_goal',assignment_2_2022.msg.PlanningAction)
	""" set the action client
	"""
	Odometry_sub = rospy.Subscriber("/odom", Odometry,sub_callback)
	""" subscribe to */odom"*
	"""
	rospy.spin()
	

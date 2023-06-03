#! /usr/bin/env python3

"""

.. module:: node_b
   :platform: Unix
   :synopsys: Documentation fro Node "B" from assignment 02 of RT1
	
..moduleauthor:: Aicha Manar ABBAD

Node 'b' implements a service to */reaching_goal/result* where it returns the number of reached or cancelled goals by the user.

Subscribes to :
	/reaching_goal/result
	
Service to :
	/reach_cancel


"""

import rospy
import assignment_2_2022.msg

from std_srvs.srv import Empty,EmptyResponse

""" Global variables definition
"""
reached_goals = 0  
""" to count the number of reached goals
"""
canceled_goals = 0 
""" to count the number of canceled goals
"""



def sub_callback(data):
	"""
	
	*sub_callbacl()* is a callback function that checks the status of the robot
	to see if the robot reached its goaled or if is cancelled.
	
	"""
	global canceled_goals
	global reached_goals
	if(data.status.status == 2):
		""" case goal canceled
		"""
		canceled_goals = canceled_goals + 1
		print("canceled goal")
		""" increment the number of cancelled goals by 1
		"""
	elif(data.status.status == 3): 
		""" case the robot reached the goal
		"""
		reached_goals = reached_goals + 1
		print("reached goal")
		""" increment the number of reached goals by 1
		"""


def srv_callback(req):
	
	"""
	
	*srv_callback()* is a service callback function that returns the number or reached and canceled goals.
	
	"""
	global canceled_goals
	global reached_goals
	print(f"The number of reached goals is : {reached_goals} \nnumber of canceled goals is : {canceled_goals}")
	""" print the number of reached and cancelled goals
	"""
	return EmptyResponse()	



if __name__ == "__main__":
	rospy.init_node("node_b") 
	"""initialize the node
	"""
	service = rospy.Service("reach_cancel", Empty, srv_callback)
	""" Create a service to *reach_cancel*
	"""
	subscribe = rospy.Subscriber('/reaching_goal/result', assignment_2_2022.msg.PlanningActionResult, sub_callback)
	""" Subscribes to * /reaching_goal/result*
	"""
	rospy.spin()


from __future__ import print_function

import time
from sr.robot import *

"""
Assignment 1 python script

It is requested to write a python node that controls the robot to put all the golden tokens togheter.

My personal implementation has the following steps:
	- 1) count how many tokens there are in the arena and put their IDs in a list.
	- 2) set as reference token the first token saw and save its ID.
	- 3) search the unpaired token and grab it.
	- 4) find the reference token.
	- 5) release the unpaired token near to reference token.
	- 6) repeat 3-5 steps until there are no more unpaired tokens.

To read better what the robot do, I added a simple delay between actions to avoid annoying movement messages.
I could turn down the velocities and the times of drive and turn functions but the robot would be too slow.
One of the valutation point of the assignment doesn't include the time to reach the goal but i prefer to speed up the robot.
	
"""
a_th = 5.0
""" float: Threshold for the control of the orientation """

d_th = 0.4
""" float: Threshold for the control of the linear distance """

R = Robot()
""" instance of the class Robot """

p_th = 2
""" int: Threshold for release the unpaired token to the reference token  """

delay = 5
""" int: delay time to read better what the robot do. """

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args:
		speed (int): the speed of the wheels
		seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args:
		speed (int): the speed of the wheels
		seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
				
def rotation(rot_y):
	"""
	Function to adjust the robot's direction with respect to the token
        
	Args: rot_y (float): rotation about the Y axis in degrees
	"""
	if -a_th <= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("Ah, here we are!.")
		drive(40, 0.05)
	elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left
		print("Left a bit...")
		turn(-10, 0.05)
	elif rot_y > a_th: # if the robot is not well aligned with the token, we move it on the right
		print("Right a bit...")
		turn(+10, 0.05)
	return rot_y

def count_token():
	"""
	Function to count how many tokens there are in arena and save their IDs in a list.
	The first token saw it will be the reference token.
	
	Returns:
		n (int): numbers of tokens
		id_list (list): list of token IDs
		reference_id (int): ID of the reference token
	"""
	id_list = []
	dist=100
	for i in range(12): # The Robot goes around 360 degrees
		print("I'm scanning the arena.")
		for token in R.see():
			if token.info.code not in id_list: # Save in a list all token IDs saw, only if the ID it's not already present there
				id_list.append(token.info.code)
		turn(20,0.5)
		
	n = len(id_list) # Numbers of tokens in the arena
	print("There are",n,"tokens in the arena and their IDs are:",id_list)
	
	reference_id = id_list[0] # Set the first token and saw as reference token
	print("The reference token ID is:",reference_id)
	
	id_list.remove(reference_id) # Remove from id_list the reference token ID
	m = len(id_list) # Numbers of unpaired tokens
	print("There are", m,"unpaired tokens and their IDs are:", id_list)
	
	return id_list, reference_id # Return the id_list of unpaired token and there ID of reference token

	
def find_token(id_list, reference_id):
	"""
	Function to find unpaired token.
	
	Args:
		id_list (list): list of token IDs
		reference_id (int): ID of the reference token
	
	Return:
		id_list (list): list of token IDs
	"""
	dist=100
	while True:
		for token in R.see():
			if token.info.code != reference_id and token.info.code in id_list and token.dist < dist: # Search
				dist = token.dist
				rot_y = token.rot_y
		if dist==100:
			print("I don't see unpaired token!")
			turn(-50,0.05);
		elif dist < d_th: 
			print("Unpaired token Found!")
			if R.grab(): # if we are close to the token, we grab it.
				print("I got the token with ID:",token.info.code)
				time.sleep(delay)
				
				find_reference(reference_id) # Find the reference token to release near it the token just got
				
				id_list.remove(token.info.code) # Remove from unpareid token IDs list the token ID just paired
				print("I removed from id_list the token with ID:",token.info.code)
				print("The new list is:",id_list)
				print("Other", len(id_list),"tokens to pair.")
				time.sleep(delay)
				
			else:
				print("I'm not close enough");
		elif -a_th <= rot_y <= a_th or rot_y < -a_th or rot_y > a_th:
			rot_y = rotation(rot_y)
		return id_list
	return 1
	
def find_reference(reference_id):
	"""
	Function to find the reference token.
	
	Args:
		reference_id (int): reference token ID
	"""
	dist=100
	while True:
		for token in R.see():
			if token.info.code is reference_id:# and token.dist < dist:
				dist = token.dist
				rot_y = token.rot_y
		if dist==100:
			print("I don't see the reference token!!")
			turn(-50,0.05); #50 0.05
		elif dist < 2*d_th: 
			print("Reference token found!")
			if R.release(): # if we are close to the token, we release it.
				print("Token paired!");
				drive(-30,1)
				turn(30,2)
				break
		elif -a_th <= rot_y <= a_th or rot_y < -a_th or rot_y > a_th:
			rot_y = rotation(rot_y)
	return 1
		
def main():
	id_list, reference_id = count_token()
	time.sleep(delay)
	while id_list:
		id_list = find_token(id_list, reference_id)
	print("There are no more unpaired tokens!")
		
main()


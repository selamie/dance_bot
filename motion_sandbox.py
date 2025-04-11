import numpy as np 
import time
from frankapy import FrankaArm # import franka arm
# from frankapy_extensions import * # for task 5 (optional)

fa = FrankaArm()

# reset joints:
fa.reset_joints()

def apply_xrot(rad,pose):
	xrot = np.array([[1,0,0],[0,np.cos(rad),-np.sin(rad)],[0,np.sin(rad),np.cos(rad)]])
	new = pose@xrot
	return new

fa.goto_pose

# Write your code below:
import pdb; pdb.set_trace()
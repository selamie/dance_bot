import numpy as np 
import time
from frankapy import FrankaArm # import franka arm
from robomail.motion import GotoPoseLive
from frankapy import FrankaConstants as FC 
import copy

def apply_xrot(rad,pose):
	xrot = np.array([[1,0,0],[0,np.cos(rad),-np.sin(rad)],[0,np.sin(rad),np.cos(rad)]])
	new = pose@xrot
	return new


fa = FrankaArm()
fa.reset_joints()

controller = GotoPoseLive()

input("press enter to start dance!")

# reset joints:

# List of waypoints as numpy arrays with additional in-between points for a smoother dance
waypoints = [
    np.array([0.5, -0.2, 0.2]),  # Bottom-left middle
    np.array([0.5, 0.0, 0.2]),   # Center bottom
    np.array([0.5, 0.2, 0.2]),   # Bottom-right middle
    np.array([0.6, 0.2, 0.3]),   # Slight raise
    np.array([0.7, 0.0, 0.4]),   # Top far center
    np.array([0.6, -0.1, 0.5]),  # Diagonal transition
    np.array([0.3, 0, 0.4]),     # Top near center
    np.array([0.4, 0.1, 0.5]),   # Smooth transition
    np.array([0.5, -0.2, 0.6]),  # Top-left middle
    np.array([0.5, 0.0, 0.5]),   # Center top
    np.array([0.5, 0.2, 0.6]),   # Top-right middle
    np.array([0.4, 0.1, 0.3]),   # Lowering motion
    np.array([0.35, -0.2, 0.2])   # Reset to start
]

pose = FC.HOME_POSE.copy()
controller.set_goal_pose(pose)
controller.start()


for i,p in enumerate(waypoints): 
    # pose = controller.fa.get_pose()
    pose.translation = p
    controller.set_goal_pose(pose)
        # while np.linalg.norm(pose_controller.fa.get_pose().translation - move_to_pose.translation) > 0.05:
    while np.linalg.norm(controller.fa.get_pose().translation - p) > 0.03:
        time.sleep(0.25)


controller.stop()
# Write your code below:
# import pdb; pdb.set_trace()


# choose 30 sec sequence
# get timing from audio file (intensity)
# give times to chatgpt, populate with position
# (optional) fit to spline, re-sample 
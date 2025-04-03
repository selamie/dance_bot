import numpy as np 
import time
from frankapy import FrankaArm # import franka arm
from robomail.motion import GotoPoseLive
from frankapy import FrankaConstants as FC 
import copy

from sample_from_spline import spline_resample, waypoints, timestamps
from audio_analysis import analyze_audio, format_time
from query_gpt import queryGPT_waypoints

# reset joints:
fa = FrankaArm()
fa.reset_joints()

# print(len(waypoints), " ", len(timestamps))
timestamps, timing = analyze_audio("suavemente.mp3")

waypoints = [-1]
print(len(timestamps))
while len(waypoints) != len(timestamps):
    waypoints = queryGPT_waypoints(timestamps)
    print(len(waypoints), " ", len(timestamps))

print("waypoints match timestamps")
waypoints = np.array(waypoints)

trajectory, dt = spline_resample(waypoints, timestamps)
print(trajectory[0:10])
print("dt: ", round(dt,3))
dt = round(dt,3)
controller = GotoPoseLive()
controller.start()

print(f"song snippet starts and ends at: {format_time(timing[0])}, {format_time(timing[1])}")
input("press enter to start dance!")

pose = FC.HOME_POSE.copy()
for i,p in enumerate(trajectory): 
    print(i)
    # pose = controller.fa.get_pose()
    pose.translation = p
    controller.set_goal_pose(pose)
    # while np.linalg.norm(controller.fa.get_pose().translation - p) > 0.03:
    time.sleep(dt)

#save trajectory: 



controller.stop()
# Write your code below:
# import pdb; pdb.set_trace()


# choose 30 sec sequence
# get timing from audio file (intensity)
# give times to chatgpt, populate with position
# (optional) fit to spline, re-sample 
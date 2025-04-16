import numpy as np 
import time
from frankapy import FrankaArm # import franka arm
from robomail.motion import GotoPoseLive
from frankapy import FrankaConstants as FC 
from rospy import Rate
from sample_from_spline import spline_resample, spline_resample_euler
from autolab_core import RigidTransform, transformations
from query_gpt import extract_waypoints

from openai import OpenAI


"""This file is primarily used for testing purposes, so edits can be made to prompts,
parts of the pipeline can be tested, or waypoints can be manually tested """

MANUAL_WAYPTS = np.array([
 [0.55,  0.0,   0.4,   0.0,   0.0,   0.0,   0.34829932],
 [0.57,  0.05,  0.42,  5.0,   -5.0,  5.0,   0.81269841],
 [0.59,  0.1,   0.44,  10.0,  -10.0, 10.0,  1.10294785],
 [0.61,  0.05,  0.46,  15.0,  -15.0, 15.0,  1.40480726],
 [0.63,  0.0,   0.48,  20.0,  -20.0, 20.0,  1.71827664],
 [0.65, -0.05,  0.5,   25.0,  -25.0, 25.0,  2.03174603],
 [0.67, -0.1,   0.52,  20.0,  -20.0, 20.0,  2.33360544],
 [0.69, -0.05,  0.54,  15.0,  -15.0, 15.0,  3.55265306],
 [0.7,   0.0,   0.56,  10.0,  -10.0, 10.0,  3.86612245],
 [0.68,  0.05,  0.58,  5.0,   -5.0,  5.0,   4.16798186],
 [0.66,  0.1,   0.6,   0.0,    0.0,  0.0,   4.46984127],
 [0.64,  0.05,  0.58, -5.0,    5.0, -5.0,   4.78331066],
 [0.62,  0.0,   0.56, -10.0,  10.0, -10.0,  5.08517007],
 [0.6,  -0.05,  0.54, -15.0,  15.0, -15.0,  5.39863946],
 [0.58, -0.1,   0.52, -20.0,  20.0, -20.0,  5.70049887],
 [0.56, -0.05,  0.5,  -25.0,  25.0, -25.0,  6.31582766],
 [0.54,  0.0,   0.48, -20.0,  20.0, -20.0,  8.45206349],
 [0.52,  0.05,  0.46, -15.0,  15.0, -15.0,  9.68272109],
 [0.5,   0.1,   0.44, -10.0,  10.0, -10.0, 10.14712018],
 [0.48,  0.05,  0.42, -5.0,    5.0,  -5.0, 10.5999093],
 [0.46,  0.0,   0.4,   0.0,    0.0,   0.0, 10.90176871],
 [0.48, -0.05,  0.38,  5.0,   -5.0,   5.0, 11.2152381],
 [0.5,  -0.1,   0.36, 10.0,  -10.0,  10.0, 11.51709751],
 [0.52, -0.05,  0.34, 15.0,  -15.0,  15.0, 11.83056689],
 [0.54,  0.0,   0.32, 20.0,  -20.0,  20.0, 12.1324263],
 [0.56,  0.05,  0.3,  25.0,  -25.0,  25.0, 12.58521542],
 [0.58,  0.1,   0.32, 20.0,  -20.0,  20.0, 13.04961451],
 [0.6,   0.05,  0.34, 15.0,  -15.0,  15.0, 13.3630839],
 [0.62,  0.0,   0.36, 10.0,  -10.0,  10.0, 13.66494331],
 [0.64, -0.05,  0.38,  5.0,   -5.0,   5.0, 15.04653061],
 [0.66, -0.1,   0.4,   0.0,    0.0,   0.0, 16.10303855],
 [0.68, -0.05,  0.42, -5.0,    5.0,  -5.0, 16.41650794],
 [0.7,   0.0,   0.44,-10.0,   10.0, -10.0, 16.72997732],
 [0.68,  0.05,  0.46,-15.0,   15.0, -15.0, 17.03183673],
 [0.66,  0.1,   0.48,-20.0,   20.0, -20.0, 17.48462585],
 [0.64,  0.05,  0.5, -25.0,   25.0, -25.0, 17.94902494],
 [0.62,  0.0,   0.52,-20.0,   20.0, -20.0, 18.26249433],
 [0.6,  -0.05,  0.54,-15.0,   15.0, -15.0, 18.55274376],
 [0.58, -0.1,   0.56,-10.0,   10.0, -10.0, 18.86621315],
 [0.56, -0.05,  0.58, -5.0,    5.0,  -5.0, 19.16807256],
 [0.54,  0.0,   0.6,   0.0,    0.0,   0.0, 19.94594104],
 [0.52,  0.05,  0.58,  5.0,   -5.0,   5.0, 20.39873016],
 [0.5,   0.1,   0.56, 10.0,  -10.0,  10.0, 20.70058957],
 [0.48,  0.05,  0.54, 15.0,  -15.0,  15.0, 20.96761905],
 [0.46,  0.0,   0.52, 20.0,  -20.0,  20.0, 21.31591837],
 [0.48, -0.05,  0.5,  25.0,  -25.0,  25.0, 21.93124717],
 [0.5,  -0.1,   0.48, 20.0,  -20.0,  20.0, 22.39564626],
 [0.52, -0.05,  0.46, 15.0,  -15.0,  15.0, 22.84843537],
 [0.54,  0.0,   0.44, 10.0,  -10.0,  10.0, 23.41732426],
 [0.56,  0.05,  0.42,  5.0,   -5.0,   5.0, 24.06748299],
 [0.58,  0.1,   0.4,   0.0,    0.0,   0.0, 24.84535147],
 [0.6,   0.05,  0.38, -5.0,    5.0,  -5.0, 25.29814059],
 [0.62,  0.0,   0.36,-10.0,   10.0, -10.0, 25.86702948],
 [0.64, -0.05,  0.34,-15.0,   15.0, -15.0, 26.8306576],
 [0.66, -0.1,   0.32,-20.0,   20.0, -20.0, 27.28344671],
 [0.68, -0.05,  0.3, -25.0,   25.0, -25.0, 28.35156463],
 [0.7,   0.0,   0.32,-20.0,   20.0, -20.0, 29.73315193]
])

def querygpt_custom(customize,timestamps,use_orientation = True, max_degrees=30):
    api_key = "sk-BmKxDbClXUMnzJCMo12rLA"
    client = OpenAI(api_key=api_key,
                    base_url="https://cmu.litellm.ai")
    
    if not use_orientation: 
        #translation only base_prompt
        base_prompt = f"""You are choreographing a dance for a robot mounted to a table. You will help me generate the waypoints of this dance. 
        The allowable workspace for the robot is within the bounds of a 3-D rectangle. 
        The x,y,z coordinates of this bounded rectangle are: 
        \n\n[[0.35,-0.2,0.2], [0.35,0.2,0.2], [0.35,-0.2,0.6], [0.35,0.2,0.6], [0.7,-0.2,0.2], [0.7,0.2,0.2], [0.7,-0.2,0.6], [0.7,0.2,0.6]]
        \n Your response should also follow the format of the workspace bounds, which is a list of lists. 
        \n Respond with a plan of [x,y,z,t] waypoints for the dance in a list of arrays, with each waypoint corresponding to a timestamp 't' from the list below. 
        \n\nIn addition, we have a list of timestamps in seconds at which the movements should occur: 
        \n\n {timestamps} \n"""

    elif use_orientation:
        #orientation base_prompt
        base_prompt = f"""You are choreographing a dance for a robot mounted to a table. You will help me generate the waypoints of this dance. 
        The allowable workspace for the robot is within the bounds of a 3-D rectangle. 
        The x,y,z coordinates of this bounded rectangle are: 
        \n\n[[0.35,-0.15,0.2], [0.35,0.15,0.2], [0.35,-0.15,0.6], [0.35,0.15,0.6], [0.7,-0.15,0.2], [0.7,0.15,0.2], [0.7,-0.15,0.6], [0.7,0.15,0.6]]
        \nFor rotation, we use euler angles (roll, pitch, yaw) with respect to the robot's home pose. Commanded angles should be between -{max_degrees} and {max_degrees} degrees. 
        \nYour response should also follow the format of the workspace bounds, which is a list of lists. 
        \nRespond with a plan of [x,y,z,roll,pitch,yaw,t] waypoints for the dance in a list of arrays, with each waypoint corresponding to a timestamp 't' from the list below. 
        \n\nHere is the list of timestamps in seconds at which the movements should occur: 
        \n\n {timestamps} \n"""

    end_prompt = """\nKeep in mind the amount of time between the timestamps when considering how far to move. The coordinates are in meters, so a jump of 0.1 corresponds to 10 centimeters. 
    \n\nRespond with only the list-of-lists of waypoints, and no other text. Start with the character `[`"""

    prompt = base_prompt + customize + end_prompt

    # print(prompt)
    completion = client.chat.completions.create(
        model="gpt-4o",  # Adjust model if needed
        messages=[{"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": prompt}],
        temperature=0
    )
    # Extract the waypoints from the response
    waypoints_text = completion.choices[0].message.content
    # print(waypoints_text)
    # print(extract_waypoints(waypoints_text))
    try: 

        waypoints = eval(extract_waypoints(waypoints_text))
        print("successfully got waypts from gpt")
        return np.array(waypoints)
    except: 
        print("couldn't extract waypts from gpt, try again")
        print(waypoints_text)
        return [-1]
    # Print or process the waypoints
    

def exec_waypts(franka, waypoints, euler_rotations =True):
    # reset joints:
    if franka == None: 
        fa = FrankaArm()
    else:
        fa = franka
    fa.reset_joints()
    # if changing base pose: fa.gotojoint()
    # base = fa.get_pose.copy()

    if euler_rotations: 
        trajectory, dt = spline_resample_euler(waypoints, num_samples = 1000)
    else:
        trajectory, dt = spline_resample(waypoints, num_samples = 1000)

    default_impedances = np.array(FC.DEFAULT_TRANSLATIONAL_STIFFNESSES + FC.DEFAULT_ROTATIONAL_STIFFNESSES)
    new_impedances = np.copy(default_impedances)
    # new_impedances[3:] = np.array([0.5, 2, 0.5])*new_impedances[3:] # reduce the rotational stiffnesses, default in gotopose live
    # new_impedances[:3] = np.array([0.5, 0.5, 1])*default_impedances[:3] # reduce the translational stiffnesse
    new_impedances[3:] = np.array([0.5, 0.5, 0.5])*new_impedances[3:] # reduce the rotational stiffnesses, default in gotopose live
    # new_impedances[:3] = np.array([0.5, 0.5, 0.5])*default_impedances[:3] # reduce the translational stiffnesse

    controller = GotoPoseLive(cartesian_impedances=new_impedances.tolist())

    controller.start()
    rate = Rate(1/dt)

    input("press enter to start dance!")

    pose = FC.HOME_POSE.copy()
    for i,p in enumerate(trajectory): 
        pose = FC.HOME_POSE.copy()
        
        pose.translation = p[0:3] 
        #you could add another transform to point the "wrist" places instead of the eef
        #possible TODO: look up delta transform for wrist to eef (prob in FC.constants)
        if euler_rotations:
            pose.rotation = (transformations.euler_matrix(p[3],p[4],p[5])[0:3,0:3])@FC.HOME_POSE.copy().rotation

        controller.set_goal_pose(pose)

        rate.sleep()

    controller.stop()
    return "successfully run"



if __name__=='__main__':
    from audio_analysis import analyze_audio
    tstamps, timing = analyze_audio("audio_files/suavemente.mp3", audio_start=0)
    # orientation_waypts = queryGPT_waypoints(tstamps,use_orientation=True)
    waypts = querygpt_custom("""This is a salsa dance, Suavemente by Elvis Crispo.
                             """,tstamps, use_orientation=False)

    # waypts = np.hstack([WAYPOINTS,TSTAMPS.reshape(-1,1)])
    # waypts = np.genfromtxt('franka_waypoints.csv',delimiter=',')
    # waypts = np.zeros((len(orientation_waypts),4))
    # waypts[:,0:3] = orientation_waypts[:,0:3]
    # waypts[:,3] = orientation_waypts[:,7]
    # spline_resample_euler(WAYPTS_EULER_DEG)

    exec_waypts(franka = None, waypoints = waypts, euler_rotations = False)
    


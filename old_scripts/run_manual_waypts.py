from execute_waypts import exec_waypts
from execute_waypts import querygpt_custom, extract_waypoints
from audio_analysis import analyze_audio
from frankapy import FrankaArm
from openai import OpenAI
import numpy as np

## an old experiment script kept for archival purposes. 
## This has to be moved back in to the main folder to run successfully due to above imports. 

def querygpt_manual(timestamps, max_degrees=30):
    api_key = "sk-BmKxDbClXUMnzJCMo12rLA"
    client = OpenAI(api_key=api_key,
                    base_url="https://cmu.litellm.ai")

    prompt = [{"role": "system", "content": """You are a robot‑dance choreographer with access to a motion‑primitive library, tempo analysis, and orientation controls. """},
                {"role":"system", "content":f"""Your capabilities are as follows: 
                 \n 3D Workspace: A bounded rectangle with coordinates \n[[0.35,-0.15,0.2], [0.35,0.15,0.2], [0.35,-0.15,0.6], [0.35,0.15,0.6], [0.7,-0.15,0.2], [0.7,0.15,0.2], [0.7,-0.15,0.6], [0.7,0.15,0.6]]
                \n For rotations, we use euler angles with  euler angles (roll, pitch, yaw) with respect to the robot's home pose. Commanded angles should be between -{max_degrees} and {max_degrees} degrees. 
                \n Motion primitives: V‑shape, circle, zig‑zag, U‑shape
                \n Can sync to dynamic peaks and tempo beats
                """},
                {"role": "user", "content": f"""Here is a list of timestamps for 
                 the first 30 s of Suavemente: {timestamps}. 
                \n Task:  
                \n1. Generate a list of lists of waypoints [x,y,z,roll,pitch,yaw,t] with each waypoint corresponding to the timestamp t
                \n2. Utilize the motion primitives.  
                \n3. Respect the workspace and angle bounds.  
                \n4. The dance should have a beginning (slow/low), middle (high‑energy), end (close to center). 
                
                Respond with a list of lists of waypoints [x,y,z,roll,pitch,yaw,t]. You should edit the timestamps t as needed to add or remove points. Rely on the tempo when there are gaps in timestamps, 
                use the existing timestamps if they are closer together in time. 
                Respond with only the list of waypoints. start with the character'['"""}]
    print(prompt)
    completion = client.chat.completions.create(
        model="gpt-4o",  # Adjust model if needed
        messages=prompt,
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


fa = FrankaArm()
fa.reset_joints()
tstamps, timing = analyze_audio("audio_files/suavemente.mp3", audio_start=0)

# control/ base prompt only
# print("querying base prompt...")
# waypts = querygpt_custom("",tstamps, use_orientation=True, max_degrees = 25)

# input("press enter to reset joints, set up your recording for base prompt")
# exec_waypts(fa, waypts, euler_rotations = True)
# fa.reset_joints()

# # prompt 2 
# print("querying prompt 2...")
# waypts = querygpt_custom("""\n\nIn addition, the song is Suavemente by Elvis Crispo, and the tempo of the song is 125bpm.
# Also think about the choreography, trying to tie together a beginning, middle and end. Choreography basics involve understanding and utilizing three core elements: time, energy, and space. These elements are used to create a dance by manipulating the speed and timing of movements, the intensity and force used in executing those movements, and the location of the dancers on the stage. Elaboration:
# Time: Consider how quickly or slowly movements are performed and when they occur within the dance.
# Energy: Explore the intensity and force used in the movements, from gentle to powerful.
# Space: Think about the physical location of dancers on the stage, including their positions, paths, and directions.
# Start with the basics: Focus on the fundamental movements and steps, gradually building upon them.
# Incorporate repetition: Using repetition can make choreography easier to learn and remember.
# Embrace improvisation: Exploring spontaneous movements can lead to new ideas and unexpected discoveries.
# Study the music: Pay attention to the rhythm, melody, and tempo to guide your choreography.
# Break down the process: Divide the choreography into sections and work on them individually.
# Find inspiration: Look around for inspiration in everyday movements, people, nature, or other art forms.   
                         
# \n You should edit the timestamps t as needed to add or remove points. Rely on the tempo when there are gaps in timestamps, use the existing timestamps if they are closer together in time. 
#                             """,tstamps, use_orientation=True, max_degrees = 22)

# input("press enter to reset joints, start prompt 2, style guidance")
# exec_waypts(fa, waypts, euler_rotations = True)
# fa.reset_joints()

# prompt 3

print("querying prompt 3...")

waypts = querygpt_custom("""\n\n In addition, the tempo is 125bpm. Also think about the choreography, trying to tie together a beginning, middle and end. Choreography basics involve understanding and utilizing three core elements: time, energy, and space. These elements are used to create a dance by manipulating the speed and timing of movements, the intensity and force used in executing those movements, and the location of the dancers on the stage. Elaboration:
\nTime: Consider how quickly or slowly movements are performed and when they occur within the dance.
\nEnergy: Explore the intensity and force used in the movements, from gentle to powerful.
\nSpace: Think about the physical location of dancers on the stage, including their positions, paths, and directions.
\nStart with the basics: Focus on the fundamental movements and steps, gradually building upon them.
\nIncorporate repetition: Using repetition can make choreography easier to learn and remember.
\nEmbrace improvisation: Exploring spontaneous movements can lead to new ideas and unexpected discoveries.
\nStudy the music: Pay attention to the rhythm, melody, and tempo to guide your choreography.
\nBreak down the process: Divide the choreography into sections and work on them individually.
\nFind inspiration: Look around for inspiration in everyday movements, people, nature, or other art forms.
\n\nSome easy dance moves that you can pick from:
\nMoving up and down
\nMoving side to side(head isolations)
\nMoving in a upside down U shape or a regular U shape
\nMoving in a circle
\nMoving in a zig zag
\n \n You should edit the timestamps t as needed to add or remove points. Rely on the tempo when there are gaps in timestamps, use the existing timestamps if they are closer together in time. 
""",tstamps, use_orientation=False)

input("Ready. press enter to start prompt 3, motion primitives, turned off rotations")
exec_waypts(fa, waypts, euler_rotations = False)
fa.reset_joints()

#prompt 4
print("querying prompt 4...")
waypts = querygpt_manual(tstamps, max_degrees=22)
input("Ready. press enter to start prompt 4, manual system prompt with motion primitives")
exec_waypts(fa, waypts, euler_rotations = True)
fa.reset_joints()



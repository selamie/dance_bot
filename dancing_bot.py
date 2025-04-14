import numpy as np 
import time
from frankapy import FrankaArm # import franka arm
from robomail.motion import GotoPoseLive
from frankapy import FrankaConstants as FC 
import copy

from sample_from_spline import spline_resample, spline_resample_orient
from audio_analysis import analyze_audio, format_time
from query_gpt import queryGPT_waypoints

class dancing_bot:
    #TODO: to avoid too many fa classes, can pass fa into init
    
    def __init__(self, audio_path = "suavemente.mp3", query_orientation = False, random_rotations = False ):
        self.query_orientation = query_orientation
        self.random_rotation = random_rotations
        self.audio_path = audio_path
        self.trajectory = None
        self.dt = 0
        self.timestamps, self.timing = analyze_audio(self.audio_path)

    def sample_from_spline(self, waypoints):
        return spline_resample(waypoints)
    
    def query_gpt(self):
        waypoints = [-1]
        while len(waypoints) != len(self.timestamps):
            waypoints = queryGPT_waypoints(self.timestamps, self.query_orientation)
            print(len(waypoints), " ", len(self.timestamps))
        return waypoints

    def load(self):
        self.waypoints = self.query_gpt()
        print("waypts shape:", self.waypoints.shape)
        self.trajectory, self.dt = self.sample_from_spline(self.waypoints)

    def run(self):
        if np.any(self.trajectory) == None: 
            return "no trajectory, load first"
        else:
            assert self.dt != 0
            fa = FrankaArm()
            fa.reset_joints()
            controller = GotoPoseLive()
            controller.start()

            input("press enter to start dance!")

            pose = FC.HOME_POSE.copy()
            for i,p in enumerate(self.trajectory): 
                print(i)
                # pose = controller.fa.get_pose()
                pose.translation = p[0:3]
                if self.random_rotation:
                    print("orientation not yet implemented")
                    break
                    # rot = quaternion_to_rotation_matrix(p[3:7])
                    # if np.abs(np.linalg.det(rot)) ==1:
                    #     print("here")
                    #     pose.rotation = rot

                controller.set_goal_pose(pose)
                # while np.linalg.norm(controller.fa.get_pose().translation - p) > 0.03:
                time.sleep(self.dt)

            controller.stop()

if __name__ == '__main__':
    bot = dancing_bot(audio_path="suavemente.mp3")
    bot.load()
    print("loaded successfully")
    bot.run()


# # reset joints:
# fa = FrankaArm()
# fa.reset_joints()

# # print(len(waypoints), " ", len(timestamps))
# timestamps, timing = analyze_audio("suavemente.mp3")

# waypoints = [-1]
# print(len(timestamps))
# while len(waypoints) != len(timestamps):
#     waypoints = queryGPT_waypoints(timestamps)
#     print(len(waypoints), " ", len(timestamps))

# print("waypoints match timestamps")
# waypoints = np.array(waypoints)

# trajectory, dt = spline_resample(waypoints, timestamps)
# print(trajectory[0:10])
# print("dt: ", round(dt,3))
# dt = round(dt,3)
# controller = GotoPoseLive()
# controller.start()

# print(f"song snippet starts and ends at: {format_time(timing[0])}, {format_time(timing[1])}")
# input("press enter to start dance!")

# pose = FC.HOME_POSE.copy()
# for i,p in enumerate(trajectory): 
#     print(i)
#     # pose = controller.fa.get_pose()
#     pose.translation = p
#     controller.set_goal_pose(pose)
#     # while np.linalg.norm(controller.fa.get_pose().translation - p) > 0.03:
#     time.sleep(dt)

# controller.stop()

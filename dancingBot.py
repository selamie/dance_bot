import numpy as np 
from frankapy import FrankaArm # import franka arm
from robomail.motion import GotoPoseLive
from frankapy import FrankaConstants as FC 
from rospy import Rate

from sample_from_spline import spline_resample, spline_resample_euler, spline_resample_bounded
from audio_analysis import analyze_audio, format_time
from query_gpt import queryGPT_waypoints
from autolab_core import transformations

class DancingBot:
    #TODO: to avoid too many fa classes, can pass fa into init
    
    def __init__(self, franka = None, audio_path = "suavemente.mp3", audio_start = None, query_orientation = True, max_deg=30):
        self.query_orientation = query_orientation
        # self.audio_path = audio_path
        self.trajectory = None
        self.dt = 0
        self.max_deg = max_deg

        # franka setup
        if franka == None:
            self.fa = FrankaArm()
        else: 
            #if using this, have to setup impedances elsewhere
            self.fa = franka
        assert isinstance(self.fa,FrankaArm)


        #done, now setup)
        self.timestamps, self.timing = analyze_audio(audio_path, audio_start)

        self.fa.reset_joints()

    def sample_from_spline(self, waypoints):
        if self.query_orientation:
            return spline_resample_euler(waypoints)
        else:
            return spline_resample(waypoints)
    
    def query_gpt(self):
        waypoints = [-1]
        while len(waypoints) != len(self.timestamps):
            waypoints = queryGPT_waypoints(self.timestamps, self.query_orientation, self.max_deg)
            print("waypts v tstamps: ", len(waypoints), " ", len(self.timestamps))
            #debugging 
            print(waypoints)
        return waypoints

    def load(self):
        self.waypoints = self.query_gpt()
        print("waypts shape:", self.waypoints.shape)
        self.trajectory, self.dt = self.sample_from_spline(self.waypoints)
    
    def set_audio(self, audio_path, audio_start = None):
        #sets a new audio path, but need to call load again
        self.timestamps, self.timing  = analyze_audio(audio_path, audio_start)
        return True
    
    def set_query(self, use_orientation, max_deg):
        self.use_orientation = use_orientation
        self.max_deg = max_deg
        #sets new query vars, but need to call load again 
        return True

    def run(self):
        if np.any(self.trajectory) == None: 
            return "no trajectory, load first"
        else:
            assert self.dt != 0
            rate = Rate(1/self.dt)
            # self.fa.reset_joints()
            print("before impedances in run of dancingbot.py")

            default_impedances = np.array(FC.DEFAULT_TRANSLATIONAL_STIFFNESSES + FC.DEFAULT_ROTATIONAL_STIFFNESSES)
            new_impedances = np.copy(default_impedances)
            new_impedances[3:] = np.array([0.5, 0.5, 0.5])*new_impedances[3:]
            controller = GotoPoseLive(cartesian_impedances=new_impedances.tolist())
            print("line 80")


            input("press enter to start dance!")

            if type(self.max_deg) == int:
                roll_min, roll_max = -self.max_deg, self.max_deg  
                pitch_min, pitch_max = -self.max_deg, self.max_deg 
                yaw_min, yaw_max = -self.max_deg, self.max_deg 
            elif type(self.max_deg) == list:
                assert len(self.max_deg) == 3
                roll_min, roll_max = -self.max_deg[0], self.max_deg[0]  
                pitch_min, pitch_max = -self.max_deg[1], self.max_deg[1] 
                yaw_min, yaw_max = -self.max_deg[2], self.max_deg[2] 

            # Arbitrary workspace limits
            x_min, x_max = 0.35, 0.7
            y_min, y_max = -0.2, 0.2
            z_min, z_max = 0.2, 0.6
            
            controller.start()
            for i, p in enumerate(self.trajectory):
                # Create a copy of the home pose
                pose = FC.HOME_POSE.copy()

                # Enforce translation limits (x, y, z)
                p[0] = np.clip(p[0], x_min, x_max)
                p[1] = np.clip(p[1], y_min, y_max)
                p[2] = np.clip(p[2], z_min, z_max)
                
                # Apply the constrained translation to the pose
                pose.translation = p[0:3]

                # Enforce rotation limits (roll, pitch, yaw)
                roll, pitch, yaw = p[3], p[4], p[5]
                
                roll = np.clip(roll, roll_min, roll_max)
                pitch = np.clip(pitch, pitch_min, pitch_max)
                yaw = np.clip(yaw, yaw_min, yaw_max)

                # Convert the clamped Euler angles back to rotation matrix and apply
                pose.rotation = (transformations.euler_matrix(roll, pitch, yaw)[0:3, 0:3]) @ FC.HOME_POSE.copy().rotation

                # Set the goal pose for the controller
                controller.set_goal_pose(pose)

                rate.sleep()

            #original
            # for i,p in enumerate(self.trajectory): 
            #     #debug
                
            #     pose = FC.HOME_POSE.copy()
            #     pose.translation = p[0:3]
            #     if self.query_orientation:
            #         pose.rotation = (transformations.euler_matrix(p[3],p[4],p[5])[0:3,0:3])@FC.HOME_POSE.copy().rotation

            #     controller.set_goal_pose(pose)
            #     # while np.linalg.norm(controller.fa.get_pose().translation - p) > 0.03:
            #     rate.sleep()

            controller.stop()            


if __name__ == '__main__':
    
    bot = DancingBot(franka=None,audio_path="suavemente.mp3", audio_start=0, query_orientation=True)
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

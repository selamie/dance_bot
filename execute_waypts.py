import numpy as np 
import time
from frankapy import FrankaArm # import franka arm
from robomail.motion import GotoPoseLive
from frankapy import FrankaConstants as FC 
import copy
from rospy import Rate
from sample_from_spline import spline_resample, spline_resample_orient


# rate = Rate(10)

WAYPOINTS = np.array([
 [0.603688086033108, -0.082553414956053, 0.4119113989118244],
 [0.6205364913215593, -0.09797828117995103, 0.45234492323433695],
 [0.6111610975263401, -0.07384732522634774, 0.4392206582967124],
 [0.5867761093379023, -0.07961594752240288, 0.4223895447889649],
 [0.6097946215606764, -0.08159310477118384, 0.4012030050469628],
 [0.607473388802289, -0.055945267912295725, 0.3833303743617232],
 [0.6189475517773761, -0.03256540373640649, 0.3680687699508629],
 [0.6516791295144341, 0.02111751208153448, 0.26362950833721766],
 [0.6349537439518217, -0.0003416538688973819, 0.27919858856578306],
 [0.6161260477951055, -0.006881656016167985, 0.301868773024661],
 [0.58793704452328, -0.005529045523164716, 0.31258052234261585],
 [0.5831502607130593, -0.02406695710924639, 0.28775990350563785],
 [0.5707383415965019, -0.0037556561751911667, 0.3063229407642809],
 [0.5536968381594202, 0.016571303697163774, 0.32302720511867017],
 [0.5679949979084454, 0.04020798776179596, 0.33519522994916734],
 [0.5741610086198475, -0.01869236292511442, 0.31849121250142454],
 [0.5101246244834516, 0.17149061918754427, 0.3917360760430409],
 [0.5593689613639253, 0.08838710524965283, 0.46798555171831796],
 [0.5971866155946358, 0.11363612490323835, 0.4585527799651396],
 [0.6045556464673638, 0.12809489476416686, 0.41628197171631104],
 [0.6094972962834394, 0.10073631770490406, 0.42804119756001113],
 [0.615536657385624, 0.07133223997310875, 0.41901031084332163],
 [0.5855455129345124, 0.07277763767875557, 0.4221140366753722],
 [0.5932908943751156, 0.10303347646723612, 0.4194263224939748],
 [0.5819216695943767, 0.07745014586560571, 0.430714588847503],
 [0.5593344577834906, 0.05355393533085169, 0.39958632425416885],
 [0.5252903306361447, 0.06229754317252709, 0.42993779665032467],
 [0.5316110318280642, 0.03301362739590692, 0.4391644752455725],
 [0.5269871657859232, 0.04032204368642074, 0.41024392981149793],
 [0.5159286011052411, 0.017105217412913515, 0.3836153948169285],
 [0.5302032441910314, 0.09949184927719879, 0.43651589607583097],
 [0.5256082338471213, 0.07209746309657508, 0.42198785180291104],
 [0.522256160824306, 0.08255705822679014, 0.3926281685938309],
 [0.5289843331182066, 0.05523350615000751, 0.3817035984170958],
 [0.5031830180464695, 0.023655523948179734, 0.36202358183850103],
 [0.49024263773930143, 0.05120784239976253, 0.32695106477204694],
 [0.4919202955688694, 0.028272178790577165, 0.3482529751014725],
 [0.5108928223267915, 0.006360204764963323, 0.34978788189799204],
 [0.5310566067832376, -0.0033096977055572033, 0.37175479718608684],
 [0.5536920564777326, -0.020219289944464043, 0.3611296787633414],
 [0.629162052808144, -0.014986236082240763, 0.37923184777531077],
 [0.6434270655776667, 0.02618918385267996, 0.3669324951186863],
 [0.6498096977362057, 0.019595592159695148, 0.3381752770792013],
 [0.6245929626889927, 0.02832336204185657, 0.3391701330151972],
 [0.6159672155863422, 0.03988940296423659, 0.3708710375358503],
 [0.5554709412549573, 0.048052070918091154, 0.3786084120900098],
 [0.5269107971035384, 0.0248222199547603, 0.3503001564355211],
 [0.5411431674830322, 0.00871088749561549, 0.3901504309780854],
 [0.5406062403053179, -0.03691427190859564, 0.424126926238787],
 [0.5070841853132815, 0.01382282429400155, 0.44712872269018133],
 [0.5757154002289759, -0.02197227568574866, 0.43943061393474075],
 [0.5419357212452441, -0.050950844565309156, 0.4311026066489415],
 [0.5841458953464009, -0.025583401526039936, 0.4595831215258497],
 [0.6121544593419725, 0.05583956343603344, 0.5028452603569138],
 [0.5720162008989326, 0.07302559542427779, 0.49085608628174476],
 [0.5560947808802603, 0.12654989381711856, 0.3998043604529918],
 [0.45038236183999236, 0.19602423252891982, 0.3442522642150855]])


TSTAMPS = np.array([
    0.34829932,  0.81269841,  1.10294785,  1.40480726,  1.71827664,  2.03174603,
    2.33360544,  3.55265306,  3.86612245,  4.16798186,  4.46984127,  4.78331066,
    5.08517007,  5.39863946,  5.70049887,  6.31582766,  8.45206349,  9.68272109,
   10.14712018, 10.5999093,  10.90176871, 11.2152381,  11.51709751, 11.83056689,
   12.1324263,  12.58521542, 13.04961451, 13.3630839,  13.66494331, 15.04653061,
   16.10303855, 16.41650794, 16.72997732, 17.03183673, 17.48462585, 17.94902494,
   18.26249433, 18.55274376, 18.86621315, 19.16807256, 19.94594104, 20.39873016,
   20.70058957, 20.96761905, 21.31591837, 21.93124717, 22.39564626, 22.84843537,
   23.41732426, 24.06748299, 24.84535147, 25.29814059, 25.86702948, 26.8306576,
   27.28344671, 28.35156463, 29.73315193
])

def quaternion_to_rotation_matrix(q):
    # Extract quaternion components from the 1x4 array
    qx, qy, qz, qw = q
    
    R = np.array([
        [1 - 2*(qy**2 + qz**2), 2*(qx*qy - qw*qz), 2*(qx*qz + qw*qy)],
        [2*(qx*qy + qw*qz), 1 - 2*(qx**2 + qz**2), 2*(qy*qz - qw*qx)],
        [2*(qx*qz - qw*qy), 2*(qy*qz + qw*qx), 1 - 2*(qx**2 + qy**2)]
    ])
    
    return R

def apply_xrot(rad,pose):
    xrot = np.array([[1,0,0],[0,np.cos(rad),-np.sin(rad)],[0,np.sin(rad),np.cos(rad)]])
    new = pose@xrot

    return new

def apply_yrot(rad, pose):
    yrot = np.array([
        [np.cos(rad), 0, np.sin(rad)],
        [0, 1, 0],
        [-np.sin(rad), 0, np.cos(rad)]
    ])
    new = pose @ yrot
    return new


def apply_zrot(rad, pose):
    zrot = np.array([
        [np.cos(rad), -np.sin(rad), 0],
        [np.sin(rad), np.cos(rad), 0],
        [0, 0, 1]
    ])
    new = pose @ zrot
    return new

def generate_rotation_array(n,degs):
    angles_deg = np.random.uniform(-degs, degs, size=n)
    angles_rad = np.deg2rad(angles_deg)
    
    axes = np.random.choice(['x', 'y', 'z'], size=n)

    result = np.empty((n, 2), dtype=object)
    result[:, 0] = angles_rad
    result[:, 1] = axes

    return result


def exec_waypts(waypoints, random_rotations = False):
    # reset joints:
    fa = FrankaArm()
    fa.reset_joints()

    # if random_rotations == False:
    #     trajectory, dt = spline_resample(waypoints)
    #     print(trajectory[0:10])
    #     print("dt: ", round(dt,3))
    #     dt = round(dt,3)
    #     controller = GotoPoseLive()
    #     controller.start()

    #     input("press enter to start dance!")

    #     pose = FC.HOME_POSE.copy()
    #     for i,p in enumerate(trajectory): 
    #         print(i)
    #         # pose = controller.fa.get_pose()
    #         pose.translation = p
    #         controller.set_goal_pose(pose)
    #         # while np.linalg.norm(controller.fa.get_pose().translation - p) > 0.03:
    #         time.sleep(dt)

    #     controller.stop()
    #     return "successfully run"

    # elif random_rotations == True:
    trajectory, dt = spline_resample(waypoints, num_samples = 200)
    if random_rotations:
        rotations = generate_rotation_array(len(trajectory),30)

    dt = round(dt,3)
    controller = GotoPoseLive()
    controller.start()

    input("press enter to start dance!")

    pose = FC.HOME_POSE.copy()
    for i,p in enumerate(trajectory): 
        pose = FC.HOME_POSE.copy()
        print(p)
        if random_rotations:
            print(rotations[i])
            r = rotations[i]
            if r[1] == 'x':
                pose.rotation = apply_xrot(r[0],pose.rotation)
            if r[1] == 'y':
                pose.rotation = apply_yrot(r[0],pose.rotation)
            if r[1] == 'z':
                pose.rotation = apply_zrot(r[0],pose.rotation)

        # pose = controller.fa.get_pose()
        pose.translation = p[0:3]
        
        controller.set_goal_pose(pose)
        # while np.linalg.norm(controller.fa.get_pose().translation - p) > 0.03:

        time.sleep(dt)

    controller.stop()
    return "successfully run"



if __name__=='__main__':
    from query_gpt import queryGPT_waypoints
    from audio_analysis import analyze_audio
    # tstamps, timing = analyze_audio("suavemente.mp3")
    # orientation_waypts = queryGPT_waypoints(tstamps,use_orientation=True)
    # waypts = queryGPT_waypoints(tstamps)

    waypts = np.hstack([WAYPOINTS,TSTAMPS.reshape(-1,1)])
    # waypts = np.genfromtxt('franka_waypoints.csv',delimiter=',')
    # waypts = np.zeros((len(orientation_waypts),4))
    # waypts[:,0:3] = orientation_waypts[:,0:3]
    # waypts[:,3] = orientation_waypts[:,7]
    exec_waypts(waypts, random_rotations = False)
    


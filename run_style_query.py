from execute_waypts import exec_waypts
from execute_waypts import querygpt_custom
from audio_analysis import analyze_audio
from frankapy import FrankaArm

fa = FrankaArm()
fa.reset_joints()
tstamps, timing = analyze_audio("audio_files/suavemente.mp3", audio_start=0)

# # style 1, salsa
waypts = querygpt_custom("""This is a salsa dance, Suavemente by Elvis Crispo, so think about how to command waypoints that are salsa-like.
                            """,tstamps, use_orientation=False, max_degrees = 25)

# input("press enter to reset joints, set up your recording for style 1")
# exec_waypts(fa, waypts, euler_rotations = True)
# fa.reset_joints()


# #style 2, subtle
# waypts = querygpt_custom("""Try to use small and subtle motions, and use an even smaller portion of the workspace while still being dynamic.   
#                             """,tstamps, use_orientation=True, max_degrees = 25)

# input("press enter to reset joints, set up your recording for style 2")
# exec_waypts(fa, waypts, euler_rotations = True)
# fa.reset_joints()

#style 3, dynamic
# waypts = querygpt_custom("""Use dynamic large motions and as much of the workspace as you can  
#                             """,tstamps, use_orientation=True, max_degrees = 15)

# input("press enter to reset joints, set up your recording for style 3")
exec_waypts(fa, waypts, euler_rotations = False)
fa.reset_joints()

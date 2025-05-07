from frankapy import FrankaArm
from robomail.motion import GotoPoseLive
from frankapy import FrankaConstants as FC 
from rospy import Rate

fa = FrankaArm()
fa.reset_joints()

controller = GotoPoseLive()

controller.start()



controller.stop()

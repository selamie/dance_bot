from dancingBot import DancingBot
from frankapy import FrankaArm

##Apr. 25 
## experiment goal: film pretty videos
## test orientations kind of
fa = FrankaArm()
fa.reset_joints()

# bot = DancingBot(franka=fa, audio_path="audio_files/my_girl.mp3", audio_start=10, query_orientation=True, max_deg = 15)
# bot.load()
# input("press enter to reset joints for My Girl (15deg) by temptations, set up recording")
# bot.run()
# fa.reset_joints()

# bot.set_audio("audio_files/fur-elise.mp3", 0)
# bot.set_query(True, 30)
# bot.load()
# input("press enter to reset joints for Fur Elise, set up recording")
# bot.run()
# fa.reset_joints()

bot = DancingBot(franka=fa, audio_path="audio_files/my_girl.mp3", audio_start=0, query_orientation=True, max_deg = 30)
# bot.load()
# input("press enter to reset joints for Suavemente, set up recording")
# bot.run()
# fa.reset_joints()

# bot.load()
# input("press enter to reset joints for Suavemente, set up recording")
# bot.run()
# fa.reset_joints()

bot.load()
input("press enter to reset joints for My Girl, set up recording")
bot.run()
fa.reset_joints()

# bot2 = DancingBot(franka=fa, audio_path="audio_files/my_girl.mp3", audio_start = 10, query_orientation=True, max_deg = [30,30,15])

# bot2.load()
# input("Set up recording, then press enter to start my girl w/custom angles")
# bot2.run()
# fa.reset_joints()

# bot.set_audio("audio_files/fur-elise.mp3", 0)
# bot.load()
# input("Set up recording, then press enter to start Fur Elise")
# bot.run()
# fa.reset_joints()

# bot.set_audio("audio_files/skutababa.mp3", 120)
# bot.load()
# input("Set up recording, then press enter to start Skutababa")
# bot.run()
# fa.reset_joints()

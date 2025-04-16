from dancingBot import DancingBot
from frankapy import FrankaArm

##
fa = FrankaArm()
fa.reset_joints()
bot = DancingBot(franka=fa, audio_path="audio_files/suavemente.mp3", audio_start=30, query_orientation=True)

bot.load()
input("press enter to reset joints for Suavemente, set up recording")
bot.run()
fa.reset_joints()

bot.set_audio("audio_files/fur-elise.mp3", 0)
bot.load()
input("press enter to reset joints for Fur Elise, set up recording")
bot.run()
fa.reset_joints()

bot.set_audio("audio_files/skutababa.mp3", 120)
bot.load()
input("press enter to reset joints for Skutababa, set up recording")
bot.run()
fa.reset_joints()

bot2 = DancingBot(franka=fa, audio_path="audio_files/suavemente.mp3", audio_start = 30, query_orientation=False)

bot.load()
input("Set up recording, then press enter to start Suavemente")
bot.run()
fa.reset_joints()

bot.set_audio("audio_files/fur-elise.mp3", 0)
bot.load()
input("Set up recording, then press enter to start Fur Elise")
bot.run()
fa.reset_joints()

bot.set_audio("audio_files/skutababa.mp3", 120)
bot.load()
input("Set up recording, then press enter to start Skutababa")
bot.run()
fa.reset_joints()

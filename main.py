from dancingBot import DancingBot

##
bot = DancingBot(franka=None,audio_path="audio_files/suavemente.mp3", audio_start=30, query_orientation=True)
bot.load()
input("Set up recording, then press enter to start Suavemente")
bot.run()

bot.set_audio("audio_files/fur-elise.mp3",0)
bot.load()
input("Set up recording, then press enter to start Fur Elise")
bot.run()

bot.set_audio("audio_files/skutababa.mp3", 120)
bot.load()
input("Set up recording, then press enter to start Skutababa")
bot.run()
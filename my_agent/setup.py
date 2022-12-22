from shutil import copyfile
import os

name = os.getlogin()
text = ["agent.py", "websocket.py", "mobs.py", "command.py","blocks.py","player.py"]
for i in range(len(text)):
    copyfile(r"C:/Users/" + name + r"/Desktop/my_agent/packs/" + text[i],
             r"C:/Users/" + name + r"/AppData/Local/Programs/Python/Python311/Lib/" + text[i])
print("Done!")

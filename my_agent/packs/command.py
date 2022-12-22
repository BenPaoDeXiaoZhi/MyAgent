import websocket
import ast


class Event:
    def __init__(self):
        self.BlockBroken = "BlockBroken"
        self.BlockPlaced = "BlockPlaced"
        self.ItemUsed = "ItemUsed"
        self.PlayerMessage = "PlayerMessage"
        self.ScreenChanged = "ScreenChanged"
        self.PlayerTravelled = "PlayerTravelled"
        self.PlayerDied = "PlayerDied"


class Command:
    def __init__(self, ws):
        self.ws = ws
        self.event = Event()

    def player_pos(self, x):
        return "~%s" % x

    def run_command(self, command):
        if command[0] == '/':
            command = str(command[1:])
        self.ws.run_command(command)

    def get_nbt(self, my_list):
        my_str = str()
        if type(my_list) == list:
            for i in range(len(my_list)):
                my_str += str(my_list[i])
                my_str += ", "
        else:
            my_str = str(my_list)
        return my_str.replace("\'", "\"")

    def wait_for_data(self, sub_type, blocking=False):
        msg = self.ws.wait_for_data(sub_type, blocking)
        if msg:
            mdict = ast.literal_eval(msg)
            if sub_type == self.event.PlayerMessage:
                return mdict["body"]
            elif sub_type == self.event.ItemUsed:
                try:
                    return mdict["body"]["item"]
                except:
                    return mdict["body"]["tool"]
            elif sub_type == self.event.BlockPlaced:
                return mdict["body"]["block"]
            elif sub_type == self.event.BlockBroken:
                return mdict["body"]["block"]

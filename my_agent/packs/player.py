import ast

class Pos:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


class Player:
    def __init__(self, ws):
        self.ws = ws
        self.pos = Pos()
        while True:
            self.mdict = self.get_value()
            if self.mdict:
                self.pos.x = self.mdict["body"]["destination"]["x"]
                self.pos.y = self.mdict["body"]["destination"]["y"]
                self.pos.z = self.mdict["body"]["destination"]["z"]
                break


    def get_value(self):
        data = self.ws.run_command("tp @s @s")
        if data:
            return ast.literal_eval(data)
        else:
            return False
class Blocks:
    def __init__(self, ws):
        self.ws = ws

    def fill(self, from_x, from_y, from_z, to_x, to_y, to_z, block):
        self.ws.run_command("fill %s %s %s %s %s %s %s" % (from_x, from_y, from_z, to_x, to_y, to_z, block))

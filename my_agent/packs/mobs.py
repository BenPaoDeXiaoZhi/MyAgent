import websocket


class Mob:
    def __init__(self, ws):
        self.ws = ws

    def summon(self, animal, x="~", y="~", z="~"):
        self.ws.run_command("summon %s %s %s %s" % (animal, x, y, z))

    def kill(self, target="@e"):
        self.ws.run_command("kill %s" % target)

import websocket
import socket


class Agent:
    def __init__(self, ws):
        self.ws = ws  # 建立websocket链接
        self.ws.run_command("agent create")  # 生成agent
        self.forward = "forward"
        self.right = "right"
        self.left = "left"
        self.up = "up"
        self.back = "back"
        self.down = "down"

    def move(self, direct):
        self.ws.run_command("agent move " + direct, 0.05)  # 移动

    def place(self, item_slot, direct):
        self.ws.run_command("agent place %s %s" % (item_slot, direct), 0.05)  # 放置

    def tp(self, x="~", y="~", z="~"):
        self.ws.run_command("agent tp %s %s %s" % (x, y, z))  # 传送

    def turn(self, direct):
        self.ws.run_command("agent turn %s" % direct, 0.04)  # 转向

    def collect(self, item="all"):
        self.ws.run_command("agent collect %s" % item)  # 收集

    def drop(self, item_slot):
        self.ws.run_command("agent drop %s" % item_slot)  # 丢弃

    def setitem(self, item_slot, item, count, aux=0):
        self.ws.run_command("agent setitem %s %s %s %s" % (item_slot, item, count, aux))  # 将方块放入物品栏

    def destroy(self, direct):
        self.ws.run_command("agent destroy %s" % direct, 0.05)

    def remove(self):
        self.ws.run_command("agent remove")

    def get_pos(self):
        self.ws.run_command("agent getposition")

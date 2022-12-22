import agent

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':  # an example | 一个例子
    agent = agent.agent()   # summon agent | 生成agent(代理机器人)
    agent.tp(y = "~3")      # tp agent to ~~3~ | 将agent传送到~~3~
    for k in range(3):
        for j in range(5):
            for i in range(10):
                agent.place(1,agent.back)  # agent place back(using item 1) | agent将第一个物品栏的方块放在后面
                agent.move(agent.up)       # agent move up | agent向上移动
            agent.place(1,agent.back)
            agent.move(agent.right)        # agent move right | agent向右移动
            for i in range(10):
                agent.place(1,agent.back)
                agent.move(agent.down)     # agent move down | agent向下移动
            agent.place(1,agent.back)
            agent.move(agent.right)
        agent.move(agent.left)             # agent move left | agent向左移动
        agent.turn(agent.left)             # agent turn left | agent向左转
"""result|结果:
   1 2 3 4 5 6 7 8 9 10
1  # # # # # # # # # #
2  # . . . . . . . . #
3  # . . . . . . . . #
4  # . . . . . . . . #
5  # . . . . . . . . #
6  # . . . . . . . . #
7  # . . . . . . . . #
8  # . . . . . . . . #
9  # . . . . . . . . #
10 # . . . . . . . . #
.=air|空气
#=block|方块"""

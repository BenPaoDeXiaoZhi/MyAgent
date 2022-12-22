import math
import os
import random
import time

try:
    import base64
except:
    os.system("pip install base64")

try:
    import socket
except:
    os.system("pip install socket")

try:
    import hashlib
except:
    os.system("pip install hashlib")

try:
    import struct
except:
    os.system("pip install struct")

try:
    import time
except:
    os.system("pip install time")


class WebSocket:
    def __init__(self, port, debug = False):  # 初始化
        self.debug = debug
        self.MaxBytes = 1024 * 1024
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.server = self.init()
        self.client, self.addr = self.server.accept()

        data = self.unlock(self.client.recv(1024 * 1024))[0]
        self.web_socket_open(data, self.client)
        print(self.addr, "connect on|连接上了")
        print("===============分割线================")
        self.run_command(str("say 成功与%s:%s链接" % (self.host, self.port)))

    def send_msg(self, msg_bytes, have_data=False):  # 发送信息

        token = b"\x81"
        length = len(msg_bytes)
        if length < 126:
            token += struct.pack("B", length)
        elif length == 126:
            token += struct.pack("!BH", 126, length)
        else:
            token += struct.pack("!BQ", 127, length)

        msg = token + msg_bytes
        self.client.send(msg)

        if self.debug:print("ok!")
        data = None
        if self.debug:print("开始监听......")
        if have_data:
            self.client.setblocking(True)
            mstr = self.client.recv(1024 ** 2)
            if mstr:
                data = mstr
        if self.debug:print("监听完成")
        if data:
            if self.debug:print("收到返回值，开始解析")
            try:
                msg = self.parse_payload(data)
                if self.debug:print("value is|返回值为:%s,主要内容为:%s" % (msg, self.get_end(msg)))
                return msg
            except:
                if self.debug:print("解析失败")
                if self.debug:print(data)
        if self.debug:print("===============分割线================")
        return True

    def unlock(self, mstr):  # 头文件解码
        try:
            return mstr.decode(), "by utf8"
        except:
            return mstr.decode("gbk"), "by gbk"

    def parse_payload(self, info):  # 解码
        try:
            return info.decode()
        except:
            pass
        payload_len = info[1] & 127
        if payload_len == 126:
            extend_payload_len = info[2:4]
            mask = info[4:8]
            decoded = info[8:]
        elif payload_len == 127:
            extend_payload_len = info[2:10]
            mask = info[10:14]
            decoded = info[14:]
        else:
            extend_payload_len = None
            mask = info[2:6]
            decoded = info[6:]

        bytes_list = bytearray()
        for i in range(len(decoded)):
            chunk = decoded[i] ^ mask[i % 4]
            bytes_list.append(chunk)
        try:
            body = str(bytes_list, encoding='utf-8')
        except:
            body = str(bytes_list, encoding='gbk')
        return body

    def init(self):  # 建立websocket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("已启动....|is start....")
        for i in range(11):
            s = str("■" * i + "□" * (10 - i))
            print(("\r系统初始化:%s %s/10" % (s,i)), end="", flush=True)
            time.sleep(random.randint(1,5)/10)
        print("")
        server.settimeout(None)
        try:
            server.bind((self.host, self.port))
            server.listen(1)
            print("开始监听....|listening....")
        except:
            input("ip或port错误，即将退出（回车）")
            exit()

        print("write command|输入命令:/connect " + self.host + ":" + str(self.port))
        return server

    def get_end(self, mstr: str):  # 获取结果
        pos = mstr.find("\"statusMessage\":")
        if (pos + 1):
            end_pos = str(mstr[pos:]).find("}")
            return mstr[pos:(end_pos + pos)]
        else:
            pos = mstr.find("\"message\":")
            if (pos + 1):
                end_pos = str(mstr[pos:]).find("}")
                return mstr[pos:(end_pos + pos)]
            else:
                return mstr

    def web_socket_open(self, idata: str, client):  # 响应头
        pos = idata.find("Sec-WebSocket-Key: ") + len("Sec-WebSocket-Key: ")
        response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                       "Upgrade:websocket\r\n" \
                       "Connection: Upgrade\r\n" \
                       "Sec-WebSocket-Accept: %s\r\n" \
                       "WebSocket-Location: ws://%s%s\r\n\r\n"
        magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        value = idata[pos:pos + len("fyyi9+tqQEv3mkpjjvRWwQ==")] + magic_string
        ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
        response_str = response_tpl % (ac.decode('utf-8'), self.host, self.port)
        client.send(bytes(response_str, encoding='utf-8'))

    def run_command(self, command: str, sleep_time=0):  # 运行命令
        msg1 = """
        {\"body\": {\"origin\": {\"type\": \"player\"},\"commandLine\": \""""
        msg2 = """\",\"version\": 1},
        \"header\": {\"requestId\": \"00000000-0000-0000-0000-000000000000\",
        \"messagePurpose\": \"commandRequest\",\"version\": 1,\"messageType\": \"commandRequest\"}}"""
        if self.debug:print("发送信息: %s" % command)
        time.sleep(sleep_time)
        return self.send_msg((msg1 + command + msg2).encode(), True)


    def begin_sub(self, sub_type):
        submsg = "{\"body\":{\"eventName\": \"" + sub_type + "\" },\"header\":{\"requestId\":" \
                                                             "\"8901e7d7-2803-48ac-a5e5-c127380831ea\"," \
                                                             "\"messagePurpose\":\"subscribe\",\"version\":1," \
                                                             "\"messageType\":\"commandRequest\"}} "
        self.send_msg(submsg.encode())

    def end_sub(self, un_sub_type):
        un_submsg = "{\"body\":{\"eventName\": \"" + un_sub_type + "\" },\"header\":{\"requestId\":" \
                                                                   "\"8901e7d7-2803-48ac-a5e5-c127380831ea\"," \
                                                                   "\"messagePurpose\":\"unsubscribe\",\"version\":1," \
                                                                   "\"messageType\":\"commandRequest\"}} "
        self.send_msg(un_submsg.encode())

    def wait_for_data(self, sub, blocking = False):
        self.begin_sub(sub)
        if self.debug:print("等待数据中.....")
        data = None
        self.client.setblocking(blocking)
        try:
            data = self.parse_payload(self.client.recv(1024 ** 2))
        except:pass
        self.client.setblocking(True)
        if self.debug:print("===============分割线================")
        self.end_sub(sub)
        return data

    def end(self):
        print("即将结束...")
        self.client.settimeout(0)
        for i in range(10):
            try:self.client.recv(1024 ** 2)
            except:continue
        exit()


if __name__ == "__main__":
    print("debug open")
    magent = websocket(19143)
    magent.run_command("say hello")
else:
    print("my agent(python)")
    print("websocket is open")

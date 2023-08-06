import socket
from time import time
import threading


class message:
    def __init__(self, raw, channel, init):
        self.time = round(time())
        if not init:
            try:
                ddm = raw.split("PRIVMSG #"+channel+" :")
                self.content = ddm[1].replace("\r\n", "")
                self.author = ddm[0].split("!")[0].replace(":", "")
            except:
                pass
        else:
            self.content = None
            self.author = None


class user:
    def __init__(self,  oauth, name):
        self.sock = socket.socket()
        self.oauth = oauth
        self.name = name.lower()
        self.channel = None
    def connect(self):
        self.sock.connect(('irc.chat.twitch.tv', 6667))
    def login(self):
        self.sock.send(f"PASS {self.oauth}\n".encode('utf-8'))
        self.sock.send(f"NICK {self.name}\n".encode('utf-8'))
    def join_channel(self, channel):
        self.sock.send(f"JOIN #{channel}\n".encode('utf-8'))
        self.channel = channel
    def get_message(self, init=False):
        if self.channel is None: raise Exception("You must join a channel before getting messages!")
        raw = self.sock.recv(2048).decode('utf-8')
        resp = message(raw, self.channel, init=init)
        return resp
    def run(self, streamer, on_message=lambda *args: None, on_ready=lambda *args: None, run_threads_as_daemon=False):
        self.connect()
        self.login()
        self.join_channel(streamer)
        on_ready(streamer, self.name)
        self.get_message(True)
        self.get_message(True)
        while True:
            res = self.get_message()
            mt = threading.Thread(target=on_message, args=(res,), daemon=run_threads_as_daemon)
            mt.start()
    def send(self, content):
        if self.channel is None: raise Exception("You must join a channel before sending messages!")
        ms = bytes(":"+self.name+"!"+self.name+"@"+self.name+".tmi.twitch.tv PRIVMSG #"+self.channel+" :"+content+"\r\n", 'utf-8')
        self.sock.send(ms)

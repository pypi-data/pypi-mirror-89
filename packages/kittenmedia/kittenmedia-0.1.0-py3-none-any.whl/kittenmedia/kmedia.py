import json
import time
import re
import base64
import threading
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class SimpleEcho(WebSocket):
    onMsg = None
    _send = None
    def __init__(self, server, sock, address):
        super().__init__(server, sock, address)
        SimpleEcho._send = self.sendMessage

    def handleMessage(self):
        # echo message back to client
        # self.sendMessage(self.data)
        try:
            obj = json.loads(self.data)
            if 'jsonrpc' in obj and obj['jsonrpc'] == '2.0':
                if self.onMsg:
                    self.onMsg(obj['method'], obj['params'])
        except Exception as err:
            print(err)
            pass
    
    @staticmethod
    def sendReq(method, params={}):
        req = {
            "jsonrpc":"2.0",
            "method":method,
            "params": params
        }
        try:
            if SimpleEcho._send:
                SimpleEcho._send(json.dumps(req))
        except Exception as err:
            print("send req err", err)

    def handleConnected(self):
        ""
        # print(self.address, "connected")

    def handleClose(self):
        # print(self.address, "closed")
        SimpleEcho.sendMsg = None


class KittenMedia:
    def __init__(self, port=9989):
        self.server = SimpleWebSocketServer("", port, SimpleEcho)
        SimpleEcho.onMsg = self.onMsg
        self.image = None
        self.audio = None

    def onMsg(self, method, params):
        # print(">>>", method, params)
        if method == 'image':
            self.image = params
        elif method == 'audio':
            self.audio = params

    def stop(self):
        print("dispose")
        self.server.close()

    def wsThread(self):
        try:
            self.server.serveforever()
        except Exception as err:
            pass
            # print("WS serve", err)
            # import traceback
            # traceback.print_exc()

    def start(self):
        self.th = threading.Thread(target=self.wsThread)
        self.th.start()

    def pop(self, media='audio'):
        SimpleEcho.sendReq('pop', {'media': media})

    def waitImage(self, timeout=10):
        t0 = time.perf_counter()
        while time.perf_counter() - t0 < timeout:
            if self.image:
                img = re.sub('^data:image/.+;base64,', '', self.image['data'])
                img = base64.b64decode(img)
                self.image = None
                return img
            time.sleep(0.1)
        return None

    def waitAudio(self, timeout=10):
        t0 = time.perf_counter()
        while time.perf_counter() - t0 < timeout:
            if self.audio:
                au = base64.b64decode(self.audio['data'])
                self.audio = None
                return au
            time.sleep(0.1)
        return None




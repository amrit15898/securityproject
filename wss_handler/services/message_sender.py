import json
import pathlib
import ssl
import stomper
import time
from stomper import Frame
from threading import Thread
import websocket
import logging
import asyncio

VERSIONS = '1.0,1.1'
# sessionid = ""
username = ""
password = ""

json_data = {}


class Sender:
    destinations = {
       "/topic/return-to"
    }
    def __init__(self, url):
        self.url = url
        self.ws = websocket.WebSocketApp(self.url)
        self.ws.on_open = self._on_open
        self.ws.on_message = self._on_message
        self.ws.on_error = self._on_error
        self.ws.on_close = self._on_close
        self.opened = False

        self.connected = False

        self.counter = 0

        self._connectCallback = None
        self.errorCallback = None

    def _connect(self, timeout=0):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.load_verify_locations(pathlib.Path(__file__).with_name('chain.pem'))
        ssl_context.check_hostname = False
        thread = Thread(target=self.ws.run_forever(sslopt={'context': ssl_context}))
        thread.daemon = True
        thread.start()
        total_ms = 0
        while self.opened is False:
            time.sleep(.25)
            total_ms += 250
            if 0 < timeout < total_ms:
                raise TimeoutError(f"Connection to {self.url} timed out")

    def _on_open(self, ws_app, *args):
        ws_app.send("CONNECT\nsender:"+username+"\naccept-version:1.0,1.1,2.0\n\n\x00\n")
        i = 0
        for destination in self.destinations:
            sub = stomper.subscribe(destination, i, ack="auto")
            ws_app.send(sub)
            i+=1

        ws_app.send("SEND\ndestination:/topic/return-to\ncontent-type:application/json\n\n" + json.dumps(json_data) + "\n\x00\n")

        ws_app.send("SEND\ndestination:/app/login.addUser\ncontent-type:application/json\n\n"+json.dumps(json_data)+"\n\x00\n")

    def _on_close(self, ws_app, *args):
        self.connected = False
        logging.debug("Whoops! Lost connection to " + self.ws.url)
        self._clean_up()

    def _on_error(self, ws_app, error, *args):
        logging.debug(error)

    def _on_message(self, ws_app, msg):

        frame = stomper.Frame()
        unpacked_msg = stomper.Frame.unpack(frame, msg)
        print(unpacked_msg['cmd']+" "+unpacked_msg["body"])
        if unpacked_msg.__contains__("body"):
            if unpacked_msg["body"].__contains__("msg"):
              res = json.loads(unpacked_msg["body"])
              print(res)



    def _transmit(self, command, headers, body=None):
        out = Frame.setCmd(command, headers, body)
        logging.debug("\n>>> " + out)
        self.ws.send(out)

    def connect(self, login=None, passcode=None, headers=None, connectCallback=None, errorCallback=None,
                timeout=0):

        logging.debug("Opening web socket...")
        self._connect(timeout)

        headers = headers if headers is not None else {}
        headers['host'] = self.url
        headers['accept-version'] = VERSIONS
        headers['heart-beat'] = '10000,10000'

        if login is not None:
            headers['login'] = login
        if passcode is not None:
            headers['passcode'] = passcode

        self._connectCallback = connectCallback
        self.errorCallback = errorCallback

        self._transmit('CONNECT', headers)

    def disconnect(self, disconnectCallback=None, headers=None):
        if headers is None:
            headers = {}

        self._transmit("DISCONNECT", headers)
        self.ws.on_close = None
        self.ws.close()
        self._clean_up()

        if disconnectCallback is not None:
            disconnectCallback()

    def _clean_up(self):
        self.connected = False

    def send(self, destination, headers=None, body=None):
        print("on")
        if headers is None:
            headers = {}
        if body is None:
            body = ''
        headers['destination'] = destination
        return self._transmit("SEND", headers, body)

    def subscribe(self, destination, callback=None, headers=None):
        if headers is None:
            headers = {}
        if 'id' not in headers:
            headers["id"] = "sub-" + str(self.counter)
            self.counter += 1
        headers['destination'] = destination
        self.subscriptions[headers["id"]] = callback
        self._transmit("SUBSCRIBE", headers)

        def unsubscribe():
            self.unsubscribe(headers["id"])

        return headers["id"], unsubscribe

    def unsubscribe(self, id):
        del self.subscriptions[id]
        return self._transmit("UNSUBSCRIBE", {
            "id": id
        })

    def ack(self, message_id, subscription, headers):
        if headers is None:
            headers = {}
        headers["message-id"] = message_id
        headers['subscription'] = subscription
        return self._transmit("ACK", headers)

    def nack(self, message_id, subscription, headers):
        if headers is None:
            headers = {}
        headers["message-id"] = message_id
        headers['subscription'] = subscription
        return self._transmit("NACK", headers)

# Client("wss://192.0.3.117:9091/natsatserver/websocket").connect()

# Sender("ws://localhost:2930/server1/websocket").connect()

async def greet_every_two_seconds():
    Sender("ws://localhost:2930/server1/websocket").connect()



def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(greet_every_two_seconds())


def natsat_message_sender():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    import threading
    t = threading.Thread(target=loop_in_thread, args=(loop,))
    t.start()





def natsat_connector_message_sender(j_data, user, pwd):
    global json_data, username, password
    username=user
    password = pwd
    for i in j_data:
        json_data[i] = j_data[i]

    natsat_message_sender()




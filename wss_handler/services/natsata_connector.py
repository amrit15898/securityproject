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
import socket
import requests

VERSIONS = '1.0,1.1'
sessionid = ""
username = "dealdehradun"
deal_password = ""
packet_id = "0"

host_name = ""

class Client:
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
        ssl_context.load_verify_locations(pathlib.Path(__file__).with_name('server.pem'))
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
        json_data = {
            "sender": username,
            "password": deal_password,
            "message_subscription": packet_id
        }

        requests.post(f'http://{host_name}/wss/wss-log-change/', data={
            "username": username,
            "password": deal_password,
            "session_id": "124-44",
            "packet_id": packet_id,
            "log_message": "login successfully"
        })

        ws_app.send("SEND\ndestination:/topic/return-to\ncontent-type:application/json\n\n" + json.dumps(
            {"name": "python", "content": "login request from DEAL "}) + "\n\x00\n")

        ws_app.send("SEND\ndestination:/app/login.addUser\ncontent-type:application/json\n\n"+json.dumps(json_data)+"\n\x00\n")

    def _on_close(self, ws_app, *args):
        self.connected = False
        logging.debug("Whoops! Lost connection to " + self.ws.url)
        self._clean_up()

    def _on_error(self, ws_app, error, *args):
        print("error")
        requests.post(f'http://{host_name}/wss/wss-log-change/', data={
            "username": username,
            "password": deal_password,
            "session_id": "124-44",
            "packet_id": packet_id,
            "log_message": "logout"
        })
        logging.debug(error)

    def _on_message(self, ws_app, msg):
        frame = stomper.Frame()
        res=""
        unpacked_msg = stomper.Frame.unpack(frame, msg)
        print(unpacked_msg['cmd']+" "+unpacked_msg["body"])
        if unpacked_msg.__contains__("body"):
            if unpacked_msg["body"].__contains__("msg"):
              res = json.loads(unpacked_msg["body"])
              if res["msg"] == "Successfull Login":
                global sessionid
                sessionid = res["sessionid"]
                print(sessionid)
                # sending avalanche code update message

              else:
                 print(res["msg"])


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





async def greet_every_two_seconds():
    Client("ws://localhost:2930/server1/websocket").connect()
    # Client("wss://192.0.3.117:9091/natsatserver/websocket").connect()


def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    print("ok")
    loop.run_until_complete(greet_every_two_seconds())


def natsat_connector(usr, pwd, pk_id, host):
    # loop = asyncio.get_event_loop()
    global username, deal_password, packet_id, host_name
    username = usr
    deal_password = pwd
    packet_id = pk_id
    host_name = host
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    import threading
    t = threading.Thread(target=loop_in_thread, args=(loop,))
    t.start()



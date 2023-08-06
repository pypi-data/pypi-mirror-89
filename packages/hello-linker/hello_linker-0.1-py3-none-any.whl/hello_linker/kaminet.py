# -*- coding: utf-8 -*-
import sys
import uuid
import time
import socketio
import keyboard

DEFAULT = "KamiBot"
IP_ADRESS = "127.0.0.1"
SLEEP = 0.2
PORT = "50307"


class KamiNet:

    def __init__(self, ipaddr=IP_ADRESS, callback=None):
        self.__ipaddr = ipaddr
        self.__userid = None
        self.__cb = callback
        sio = socketio.Client()
        self.__sio = sio

        @sio.event
        def connect():
            print("Connected to server")

        @sio.event
        def connect_error():
            pass

        @sio.event
        def disconnect():
            print("Disconnected")

        @sio.event
        def handshake(msg):
            userid = str(uuid.uuid4())
            self.__sio.emit(
                "joinRoom", {"username": userid, "room": "kaminet"})

        @sio.event
        def roomUsers(msg):
            pass

        @sio.event
        def message(msg):
            # print("message", msg)
            if self.__cb is not None and msg["username"] != DEFAULT:
                self.__cb(msg["username"], msg["text"])
            self.__sio.sleep(SLEEP)

        @sio.on('my_new_message')
        def my_new_message(msg):
            pass

    def __background_task(self):
        while True:
            self.__sio.sleep(SLEEP)
            if keyboard.read_key() == "q":
                self.__sio.disconnect()
                sys.exit()

    def open(self):
        self.__sio.connect(f'http://{self.__ipaddr}:{PORT}')
        self.__sio.start_background_task(self.__background_task)
        self.__sio.wait()

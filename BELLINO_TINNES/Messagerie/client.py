#!/usr/bin/env python3
# coding: utf-8

import socket

class Client():    

    def __init__(self, pseudo):
        self.pseudo = pseudo

    def connect(self, hote, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hote, port))
        print("Connected")
    
    def sendMessage(self,message):
        self.sock.send(message.encode())
    
    def disconnect(self):
        self.sock.close()
        print("Disconnected")


client = Client("Matthieu")

client.connect("159.31.61.211",1234)

while True:
    message = input()
    client.sendMessage(message)


client.disconnect()






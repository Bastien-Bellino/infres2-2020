#!/usr/bin/env python3
# coding: utf-8

import socket
import msgpack
from Crypto import Random
from Crypto.Cipher import AES

class Client():    

    def __init__(self, pseudo, key):
        self.pseudo = pseudo
        self.key = key

    def connect(self, hote, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((hote, port))
            print("Connected")
        except:
            print("Error : Can't connect to server")

    def init(self):
        self.sock.send(self.pseudo.encode())

    def sendMessage(self,message):
        self.cipher = AES.new(self.key.encode(), AES.MODE_GCM,self.nounce)
        ciphertext, tag = self.cipher.encrypt_and_digest(message.encode())
        self.sock.send(ciphertext)
    
    def sendUnsecureMessage(self,message):
        self.sock.send(message.encode())
    
    def disconnect(self):
        self.sock.close()
        print("Disconnected")
    def setNounce(self,nounce):
        self.nounce = nounce


if __name__ == "__main__":
    client = Client("admin","8ff8aec80ea8f2a5ee5e1b6607226399")

    client.connect("159.31.61.211",1234)
    client.init()
    # Demande de mot de passe
    data = client.sock.recv(1024)
    print(data.decode() + '\n')
    message = input()
    client.sendUnsecureMessage(message)
    # Receive the nounce
    data = client.sock.recv(1024)
    print("Message recu : " + data.decode() + '\n')

    data = client.sock.recv(1024)
    print(data)
    client.setNounce(data)

    while True:
        message = input()
        client.sendMessage(message)
        data = client.sock.recv(1024)
        print("Message recu : " + data.decode() + '\n')
        

    client.disconnect()






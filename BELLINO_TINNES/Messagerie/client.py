#!/usr/bin/env python3
# coding: utf-8

import socket
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class Client():    

    def __init__(self, pseudo, key, challengeSalt):
        self.pseudo = pseudo
        self.key = key
        self.challengeSalt = challengeSalt

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
        cipher = AES.new(self.key.encode(), AES.MODE_GCM,self.nounce)
        ciphertext, tag = cipher.encrypt_and_digest(message.encode())
        self.sock.send(ciphertext)
    
    def sendUnsecureMessage(self,message):
        self.sock.send(message.encode())
    
    def disconnect(self):
        self.sock.close()
        print("Disconnected")
    def setNounce(self,nounce):
        self.nounce = nounce
    def challenge(self, password, randomString):
        temp = hashlib.sha256((password + self.challengeSalt).encode()).hexdigest()
        return hashlib.sha256((randomString.decode() + str(temp) ).encode()).hexdigest()



if __name__ == "__main__":
    client = Client("admin","8ff8aec80ea8f2a5ee5e1b6607226399","ERGH7U2S")

    client.connect("localhost",1234)
    client.init()
    # Demande de mot de passe
    data = client.sock.recv(1024)
    print(data.decode() + '\n')
    password = input()
    client.sendUnsecureMessage(password)

    # Challenge
    print("Challenge started !")
    randomString = client.sock.recv(1024) # Receive the random string
    client.sendUnsecureMessage(client.challenge(password, randomString))
    print("Challenge passed !")

    # MOTD
    data = client.sock.recv(1024)
    print("Message recu : " + data.decode() + '\n')

    # Receive the nounce
    data = client.sock.recv(1024)
    client.setNounce(data)
    print("Nounce received !")

    while True:
        message = input()
        client.sendMessage(message)
        data = client.sock.recv(1024)
        cipher = AES.new(client.key.encode(), AES.MODE_GCM,client.nounce)
        message = cipher.decrypt(data)
        print("Message recu : " + message.decode() + '\n')
        

    client.disconnect()
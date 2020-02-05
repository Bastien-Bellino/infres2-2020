#!/usr/bin/env python3

import socket
import sqlite3
import hashlib
import msgpack
from Crypto.Cipher import AES
from Crypto import Random 

class Serveur:
    def __init__(self, port, conn, c):
        self.interface = self.obtenir_interface(1, port)
        self.c = c
        self.connbd = conn
        print("Serveur Ok.")

    def obtenir_interface(self, temps_attente, port):
        interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        interface.bind(('0.0.0.0', port))
        interface.listen(5)
        return interface

    def lancement_serveur(self):
        while True:
            conn, addr = self.interface.accept()
            with conn:
                while True:
                    isConnected = 0
                    data = conn.recv(1024)
                    print(data)
                    self.c.execute('SELECT KEY, SALT FROM USERS WHERE PSEUDO=?', (data.decode(),))
                    key = c.fetchone()
                    print(key)
                    if not key:
                        return
                    msg = "Pseudo correct, entrez le mot de passe : "
                    conn.send(msg.encode())
                    mdp = conn.recv(1024)
                    mymdp = mdp.decode() + key[1]
                    myhash = hashlib.sha256(mymdp.encode()).hexdigest()
                    myhash2 = hashlib.sha256(myhash.encode()).hexdigest()
                    print(myhash2)
                    print(key[0])
                    if str(myhash2) == str(key[0]):
                        self.key = str(myhash)[:32]
                        msg = "Connection reussi"
                        conn.send(msg.encode())
                        nounce = Random.new().read(16) 
                        self.nounce = nounce
                        conn.send(nounce)
                        break
                    else:
                        return

                while True:
                    data = conn.recv(512)
                    print(self.key)
                    cipher = AES.new(self.key.encode(), AES.MODE_GCM, self.nounce)
                    text = cipher.decrypt(data)
                    text = text.decode('utf-8')

                    print("getting " + text + " from " + str(addr))
                    conn.send(text.encode())
                if not data:
                    break


if __name__ == "__main__":
    conn = sqlite3.connect('messagerie.db')
    c = conn.cursor()

    serveur = Serveur(1234, conn, c)
    serveur.lancement_serveur()
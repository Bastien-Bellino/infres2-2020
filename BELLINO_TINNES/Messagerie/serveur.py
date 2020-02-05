#!/usr/bin/env python3

import socket
import sqlite3
import hashlib
import msgpack
from Crypto.Cipher import AES
from Crypto import Random 

class Serveur:
    def __init__(self, port, conn, cursor):
        self.interface = self.obtenir_interface(1, port)
        self.cursor = cursor
        self.connbd = conn
        print("Serveur Ok.")

    def obtenir_interface(self, temps_attente, port):
        interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        interface.bind(('0.0.0.0', port))
        interface.listen(5)
        return interface

    def verifier_utilisateur(self, data):
        self.currentUser = data.decode()
        self.cursor.execute('SELECT KEY, SALT FROM USERS WHERE PSEUDO=?', (data.decode(),))
        key = self.cursor.fetchone()
        if not key:
            return 0
        else:
            return key
    
    def verifier_mot_de_passe(self, mdp, key, conn):
        mymdp = mdp.decode() + key[1]
        myhash = hashlib.sha256(mymdp.encode()).hexdigest()
        myhashhash = hashlib.sha256(myhash.encode()).hexdigest()
        if str(myhashhash) == str(key[0]):
            self.key = str(myhash)[:32]
            msg = "Connection reussi : Bienvenue " + self.currentUser
            conn.send(msg.encode())
            nounce = Random.new().read(16) # Send Nounce 
            self.nounce = nounce
            conn.send(nounce)
            return 1
        else:
            return 0

    def recevoir_message(self, conn):
        data = conn.recv(512)
        self.add_message_db(data,self.nounce,self.currentUser)
        cipher = AES.new(self.key.encode(), AES.MODE_GCM, self.nounce)
        text = cipher.decrypt(data)
        text = text.decode()
        return text

    def add_message_db(self,message,nounce,user):
        self.cursor.execute('INSERT INTO MESSAGE VALUES(?,?,?)', (message,user,nounce,))
        self.connbd.commit()

    def chiffrer_message(self, msg):
        cipher = AES.new(self.key.encode(), AES.MODE_GCM, self.nounce)
        chiffre, tag = cipher.encrypt_and_digest(msg.encode())
        return chiffre

    def lancement_serveur(self):
        while True:
            conn, addr = self.interface.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    key = self.verifier_utilisateur(data)
                    if key == 0:
                        return
                    msg = "Pseudo correct, entrez le mot de passe : "
                    conn.send(msg.encode())
                    mdp = conn.recv(1024)
                    result = self.verifier_mot_de_passe(mdp, key, conn)
                    if result == 1:
                        break
                    else:
                        return
                while True:
                    msg = self.recevoir_message(conn)
                    reponse = self.chiffrer_message(msg)
                    conn.send(reponse)
                if not data:
                    break

if __name__ == "__main__":
    conn = sqlite3.connect('messagerie.db')
    c = conn.cursor()

    serveur = Serveur(1234, conn, c)
    serveur.lancement_serveur()
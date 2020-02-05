#!/usr/bin/env python3

import socket

class Serveur:
    def __init__(self, port):
        self.interface = self.obtenir_interface(1, port)

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
                    data = conn.recv(1024)
                    print("getting " + str(data.decode()) + " from " + str(addr))
                if not data:
                    break
                conn.sendall(data)


if __name__ == "__main__":
    serveur = Serveur(1234)
    serveur.lancement_serveur()



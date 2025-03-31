import tkinter as tk
from tkinter import *
import socket
import socketserver
from threading import Thread
import json
from random import randint
from Class_plateau import Plateau
from Class_joueur import Joueur


class Client:
    def __init__(self, client_host_ip, client_host_port):
        self.__host, self.__port = "localhost", 9999
        self.__client_host_ip = client_host_ip
        self.__client_host_port = client_host_port
        self.actions = {
            'party_status': self.party_status,
            'gameboard_status': self.gameboard_status,
            'move': self.move,
            'list': self.list,
            'subscribe': self.subscribe,
        }
        self.root = tk.Tk()
        self.root.title("Client de Jeu")
        self.plateau = Plateau(5, 5, 3)
        self.joueur1 = Joueur(1, "loup", 0, 0, "OK", 0)
        self.joueur2 = Joueur(2, "villageois", 1, 1, "OK", 0)
        self.joueurs = [self.joueur1, self.joueur2]
        self.canva = tk.Canvas(self.root, width=self.plateau.get_nb_colonnes() * 40, height=self.plateau.get_nb_lignes() * 40+250)
        self.canva.pack() 
        self.draw_plateau(self.canva, self.plateau, [self.joueur1, self.joueur2])


    def draw_plateau(self, canvas, plateau, joueurs):
        cell_size = 40
        for i in range(plateau.get_nb_lignes()):
            for j in range(plateau.get_nb_colonnes()):
                x0, y0 = j * cell_size, i * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                if (j, i) in plateau.get_pos_obstacles():
                    canvas.create_rectangle(x0, y0, x1, y1, fill="red", tags="shape")
                else:
                    joueur_present = False
                    for joueur in joueurs:
                        if joueur.get_co_x() == j and joueur.get_co_y() == i:
                            joueur_present = True
                            if joueur.get_role() == "loup":
                                canvas.create_rectangle(x0, y0, x1, y1, fill="black", tags="shape")
                            elif joueur.get_role() == "villageois":
                                canvas.create_rectangle(x0, y0, x1, y1, fill="blue", tags="shape")
                            break
                    if not joueur_present:
                        canvas.create_rectangle(x0, y0, x1, y1, fill="", outline="black", tags="shape")


    def draw_bomb(self, canvas, x0, y0, x1, y1):
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2
        radius = (x1 - x0) / 4
        canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill="black")
        canvas.create_line(center_x, y0 + 10, center_x, y0 + 5, fill="red", width=2)

    def draw_smiley(self, canvas, x0, y0, x1, y1):
        canvas.create_oval(x0, y0, x1, y1, fill="yellow", outline="black")
        eye_size = (x1 - x0) / 8
        eye_x_offset = (x1 - x0) / 4
        eye_y_offset = (y1 - y0) / 4
        canvas.create_oval(x0 + eye_x_offset, y0 + eye_y_offset, x0 + eye_x_offset + eye_size, y0 + eye_y_offset + eye_size, fill="black")
        canvas.create_oval(x1 - eye_x_offset - eye_size, y0 + eye_y_offset, x1 - eye_x_offset, y0 + eye_y_offset + eye_size, fill="black")
        canvas.create_arc(x0 + eye_x_offset, y1 - eye_y_offset - eye_size, x1 - eye_x_offset, y1 - eye_y_offset, start=0, extent=-180, style=ARC, outline="black", width=2)

    def check_victoire(self,joueurs):
        villageois = []
        loups = []
        for joueur in joueurs:
            if joueur.get_role() == "villageois":
                villageois.append(joueur)
            elif joueur.get_role() == "loup":
                loups.append(joueur)
        for loup in loups:
            for villageoi in villageois:
                if loup.get_co_x() == villageoi.get_co_x() and loup.get_co_y() == villageoi.get_co_y():
                    villageoi.set_etat("KO")
                    print("villageois KO")
                    joueurs.remove(villageoi)

        def nouveau_jeu(self, taille_x, taille_y, nb_obstacle, nb_joueurs, nb_loup):
            print()
            print("----nouveau jeu----")
            plateau = Plateau(taille_x, taille_y, nb_obstacle)
            print(plateau)
            joueurs = []
            for i in range(nb_joueurs):
                x = 0
                y = 0
                while((x,y) in plateau.get_pos_obstacles()):
                        x = randint(0, taille_x - 1)
                        y = randint(0, taille_y - 1)
                if i <= nb_loup-1:
                    joueurs.append(Joueur(i, "loup", x, y, "OK", 0))
                else:
                    joueurs.append(Joueur(i, "villageois", x, y, "OK", 0))
                print()
                print("---------------")
                print(joueurs([i]))
        
            return plateau, joueurs

    def send_action(self):
        action = self.action_entry.get()
        if action in self.actions:
            response = self.actions[action]()
            messagebox.showinfo("Réponse du serveur", response)
        else:
            messagebox.showerror("Erreur", "Action non supportée")

    def __send(self, message):
        received = None
        message_to_send = f'{self.__client_host_ip},{self.__client_host_port},{message}'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.__host, self.__port))
            sock.sendall(bytes(message_to_send, "utf-8"))
            sock.sendall(b"\n")
            received = str(sock.recv(1024), "utf-8")
        return received

    def party_status(self):
        message = json.dumps({"action": "party_status", "parameters": []})
        return self.__send(message)

    def gameboard_status(self):
        message = json.dumps({"action": "gameboard_status", "parameters": []})
        return self.__send(message)

    def move(self):
        move_input = input("Entrez le déplacement (ex: '01' pour déplacer en bas à droite): ")
        message = json.dumps({"action": "move", "parameters": [{"move": move_input}]})
        return self.__send(message)

    def list(self):
        message = json.dumps({"action": "list", "parameters": []})
        return self.__send(message)

    def subscribe(self):
        player_id = input("Entrez l'ID du joueur: ")
        party_id = input("Entrez l'ID de la partie: ")
        message = json.dumps({"action": "subscribe", "parameters": [{"player": player_id, "id_party": party_id}]})
        return self.__send(message)

    def run(self):
        self.root.mainloop()
    
if __name__ == "__main__":
    client_port = int(input('client port: '))
    client = Client('localhost', client_port)
    client.run()

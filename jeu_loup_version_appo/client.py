# import tkinter as tk
# from tkinter import *
# import socket
# import socketserver
# import json
# from random import randint
# from Class_plateau import Plateau
# from Class_joueur import Joueur


# class Client:
#     def __init__(self, client_host_ip, client_host_port):
#         self.__host, self.__port = "localhost", 9999
#         self.__client_host_ip = client_host_ip
#         self.__client_host_port = client_host_port
#         self.actions = {
#             'party_status': self.party_status,
#             'gameboard_status': self.gameboard_status,
#             'move': self.move,
#             'list': self.list,
#             'subscribe': self.subscribe,
#         }
#         self.root = tk.Tk()
#         self.root.title("Client de Jeu")
#         self.plateau = Plateau(5, 5, 3)
#         self.joueur1 = Joueur(1, "loup", 0, 0, "OK", 0)
#         self.joueur2 = Joueur(2, "villageois", 1, 1, "OK", 0)
#         self.joueurs = [self.joueur1, self.joueur2]
#         self.canva = tk.Canvas(self.root, width=self.plateau.get_nb_colonnes() * 40, height=self.plateau.get_nb_lignes() * 40+250)
#         self.canva.pack() 
#         self.draw_plateau(self.canva, self.plateau, [self.joueur1, self.joueur2])
#         self.draw_vision_joueur(self.canva, self.joueur1,)

#         self.button_haut = Button(text="haut",command = lambda : self.move("haut") )
#         self.button_haut.place(x=-80+self.plateau.get_nb_colonnes() * 20, y=self.plateau.get_nb_lignes() * 40, width=160, height=50)

#         self.button_bas = Button(text="bas",command = lambda : self.move("bas"))
#         self.button_bas.place(x=-80+self.plateau.get_nb_colonnes() * 20, y=self.plateau.get_nb_lignes() * 40+100, width=160, height=50)

#         self.button_droite = Button(text="droite",command = lambda : self.move("droite"))
#         self.button_droite.place(x=self.plateau.get_nb_colonnes() * 20, y=self.plateau.get_nb_lignes() * 40+50, width=160, height=50)

#         self.button_gauche = Button(text="gauche",command = lambda :self.move("gauche"))
#         self.button_gauche.place(x=-160+self.plateau.get_nb_colonnes() * 20, y=self.plateau.get_nb_lignes() * 40+50, width=160, height=50)
    
#     def move(self, direction):
#         print("Moving in direction:", direction)
#         return direction

#     def draw_plateau(self, canvas, plateau, joueurs):
#         cell_size = 40
#         for i in range(plateau.get_nb_lignes()):
#             for j in range(plateau.get_nb_colonnes()):
#                 x0, y0 = j * cell_size, i * cell_size
#                 x1, y1 = x0 + cell_size, y0 + cell_size
#                 if (j, i) in plateau.get_pos_obstacles():
#                     canvas.create_rectangle(x0, y0, x1, y1, fill="red", tags="shape")
#                 else:
#                     joueur_present = False
#                     for joueur in joueurs:
#                         if joueur.get_co_x() == j and joueur.get_co_y() == i:
#                             joueur_present = True
#                             if joueur.get_role() == "loup":
#                                 canvas.create_rectangle(x0, y0, x1, y1, fill="black", tags="shape")
#                             elif joueur.get_role() == "villageois":
#                                 canvas.create_rectangle(x0, y0, x1, y1, fill="blue", tags="shape")
#                             break
#                     if not joueur_present:
#                         canvas.create_rectangle(x0, y0, x1, y1, fill="", outline="black", tags="shape")


#     def gameboard_status(self, canvas, vision):
#         cell_size = 40
#         j = 0
#         for i in range(len(vision)): 
#             if i % 3 == 0 and i != 0:
#                 j+=1
#             y0, x0 = j * cell_size, (i-j*3) * cell_size
#             x1, y1 = x0 + cell_size, y0 + cell_size
#             if vision[i] == "0":
#                 canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black", tags="shape")
#             elif vision[i] == "1":
#                 canvas.create_rectangle(x0, y0, x1, y1, fill="blue", tags="shape")
#             elif vision[i] == "2":
#                 canvas.create_rectangle(x0, y0, x1, y1, fill="black", tags="shape")
#             else:
#                 canvas.create_rectangle(x0, y0, x1, y1, fill="red", tags="shape")

#     # def check_victoire(self,joueurs):
#     #     villageois = []
#     #     loups = []
#     #     for joueur in joueurs:
#     #         if joueur.get_role() == "villageois":
#     #             villageois.append(joueur)
#     #         elif joueur.get_role() == "loup":
#     #             loups.append(joueur)
#     #     for loup in loups:
#     #         for villageoi in villageois:
#     #             if loup.get_co_x() == villageoi.get_co_x() and loup.get_co_y() == villageoi.get_co_y():
#     #                 villageoi.set_etat("KO")
#     #                 print("villageois KO")
#     #                 joueurs.remove(villageoi)

#         # def nouveau_jeu(self, taille_x, taille_y, nb_obstacle, nb_joueurs, nb_loup):
#         #     print()
#         #     print("----nouveau jeu----")
#         #     plateau = Plateau(taille_x, taille_y, nb_obstacle)
#         #     print(plateau)
#         #     joueurs = []
#         #     for i in range(nb_joueurs):
#         #         x = 0
#         #         y = 0
#         #         while((x,y) in plateau.get_pos_obstacles()):
#         #                 x = randint(0, taille_x - 1)
#         #                 y = randint(0, taille_y - 1)
#         #         if i <= nb_loup-1:
#         #             joueurs.append(Joueur(i, "loup", x, y, "OK", 0))
#         #         else:
#         #             joueurs.append(Joueur(i, "villageois", x, y, "OK", 0))
#         #         print()
#         #         print("---------------")
#         #         print(joueurs([i]))
        
#         #     return plateau, joueurs

#     def __send(self, message):
#         received = None
#         message_to_send = f'{self.__client_host_ip},{self.__client_host_port},{message}'
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#             sock.connect((self.__host, self.__port))
#             sock.sendall(bytes(message_to_send, "utf-8"))
#             sock.sendall(b"\n")
#             received = str(sock.recv(1024), "utf-8")
#         return received

#     def party_status(self):
#         message = json.dumps({"action": "party_status", "parameters": []})
#         return self.__send(message)
    
#     def list(self):
#         message = json.dumps({"action": "list", "parameters": []})
#         return self.__send(message)

#     def subscribe(self):
#         player_id = input("Entrez l'ID du joueur: ")
#         party_id = input("Entrez l'ID de la partie: ")
#         message = json.dumps({"action": "subscribe", "parameters": [{"player": player_id, "id_party": party_id}]})
#         return self.__send(message)

#     def run(self):
#         self.root.mainloop()
    
# if __name__ == "__main__":
#     client_port = int(input('client port: '))
#     client = Client('localhost', client_port)
#     client.run()


import grpc
import game_pb2
import game_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = game_pb2_grpc.GameServiceStub(channel)

        # Example: Party Status
        response = stub.PartyStatus(game_pb2.Empty())
        print(f"Party Status: {response}")

        # Example: Gameboard Status
        response = stub.GameboardStatus(game_pb2.Empty())
        print(f"Gameboard Status: {response}")

        # Example: Move
        response = stub.Move(game_pb2.MoveRequest(row=2, col=3))
        print(f"Move Response: {response}")

        # Example: List
        response = stub.List(game_pb2.Empty())
        print(f"List Response: {response}")

        # Example: Subscribe
        response = stub.Subscribe(game_pb2.SubscribeRequest(player_id=1, party_id=1))
        print(f"Subscribe Response: {response}")

if __name__ == "__main__":
    run()

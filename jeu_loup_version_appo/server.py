import jsonpickle
import socketserver
import socket
import json
from Class_joueur import Joueur
from Class_plateau import Plateau

class App:
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = App()
        return cls.__instance

    def __init__(self):
        self.actions = {
            'party_status': self.party_status,
            'gameboard_status': self.gameboard_status,
            'move': self.move,
            'list': self.list,
            'subscribe': self.subscribe,
        }
        self.__reload_from_disk()
        self.__init_game()
        self.board = Plateau(10, 10, 5)
        self.joueurs = []
        self.clients = set()

    def party_status(self, params):
        # Exemple de réponse pour l'état de la partie
        response = {
            "status": "OK",
            "response": {
                "party": {
                    "id_party": 1,
                    "id_player": len(self.joueurs),
                    "started": True,
                    "round_in_progress": 1,
                    "move": {
                        "next_position": {
                            "row": 0,
                            "col": 1
                        }
                    }
                }
            }
        }
        return json.dumps(response)

    def gameboard_status(self, params):
        # Exemple de réponse pour l'état du plateau
        response = {
            "status": "OK",
            "response": {
                "visible_cells": "010010000"  # Exemple de chaîne représentant le plateau
            }
        }
        return json.dumps(response)

    def move(self, params):
        # Exemple de gestion de déplacement
        move_data = json.loads(params)[0]
        move_vector = move_data["move"]
        # Logique de déplacement à implémenter
        response = {
            "status": "OK",
            "response": {
                "round_in_progress": 1,
                "move": {
                    "next_position": {
                        "row": int(move_vector[0]),
                        "col": int(move_vector[1])
                    }
                }
            }
        }
        return json.dumps(response)

    def list(self, params):
        # Exemple de réponse pour la liste des parties
        response = {
            "status": "OK",
            "response": {
                "id_parties": [1, 2, 3]
            }
        }
        return json.dumps(response)

    def subscribe(self, params):
        subscribe_data = json.loads(params)[0]
        player_id = subscribe_data["player"]
        party_id = subscribe_data["id_party"]

        new_joueur = Joueur(id=player_id, role="villageois", co_x=0, co_y=0, etat="actif", deplacement=0)
        self.joueurs.append(new_joueur)

        response = {
            "status": "OK",
            "response": {
                "role": "villageois",
                "id_player": player_id
            }
        }
        return json.dumps(response)
    
    def __del__(self):
        self.db.close()

    def run(self, action, params, client_target_ip, client_target_port):
        self.clients.add((client_target_ip, int(client_target_port)))
        return self.actions[action](params)

    def save_to_disk(self):
        # Logique de sauvegarde à implémenter
        pass

    def __init_game(self):
        # Logique d'initialisation du jeu à implémenter
        pass

    def __reload_from_disk(self):
        # Logique de rechargement depuis le disque à implémenter
        pass

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        pieces = [b'']
        total = 0
        while b'\n' not in pieces[-1] and total < 10_000:
            pieces.append(self.request.recv(2000))
            total += len(pieces[-1])
        self.data = b''.join(pieces)
        print(f"Received from {self.client_address[0]}:")
        request = self.data.decode("utf-8")
        print(f'request: {request}')
        request_split = request.split(',')

        client_target_ip, client_target_port, action = request_split[0], request_split[1], request_split[2]
        app = App.get_instance()
        response = app.run(action.strip(), ','.join(request_split[3:]), client_target_ip, client_target_port)
        self.request.sendall(str(response).encode(encoding='utf-8'))
        app.save_to_disk()

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()

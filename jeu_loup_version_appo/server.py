import jsonpickle
import socketserver
import socket
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
            "party_status": self.party_status,
            "gameboard_status": self.gameboard_status,
            "move": self.move,
            "list": self.list,
            "subscribe": self.subscribe,
            "update_board": self.update_board 
        }
        self.board = Plateau(10, 10, 5)  
        self.joueurs = [] 
        self.clients = set()

    def party_status(self, params):
        id_player = params.get("id_player")
        id_party = params.get("id_party")
        response = {
            "status": "OK",
            "response": {
                "party": {
                    "id_party": id_party,
                    "id_player": id_player,
                    "started": True,
                    "round_in_progress": 1,
                    "move": {"next_position": {"row": 0, "col": 1}}
                }
            }
        }
        return jsonpickle.encode(response)

    def gameboard_status(self, params):
        visible_cells = "0001002000"  
        response = {
            "status": "OK",
            "response": {
                "visible_cells": visible_cells
            }
        }
        return jsonpickle.encode(response)

    def move(self, params):
        id_party = params.get("id_party")
        id_player = params.get("id_player")
        move = params.get("move").split(',')
        dx, dy = int(move[0]), int(move[1])

        # Trouver le joueur
        joueur = next((j for j in self.joueurs if j.get_id() == id_player), None)
        if joueur:
            new_x = joueur.get_co_x() + dx
            new_y = joueur.get_co_y() + dy

            # Vérifier les limites du plateau et les obstacles
            if (0 <= new_x < self.board.get_nb_colonnes() and
                0 <= new_y < self.board.get_nb_lignes() and
                (new_x, new_y) not in self.board.get_pos_obstacles()):

                joueur.set_co_x(new_x)
                joueur.set_co_y(new_y)

                response = {
                    "status": "OK",
                    "response": {
                        "round_in_progress": 1,
                        "move": {"next_position": {"row": new_y, "col": new_x}}
                    }
                }
            else:
                response = {
                    "status": "KO",
                    "response": "Mouvement invalide"
                }
        else:
            response = {
                "status": "KO",
                "response": "Joueur non trouvé"
            }

        return jsonpickle.encode(response)

    def list(self, params):
        response = {
            "status": "OK",
            "response": {
                "id_parties": [1, 2, 3]
            }
        }
        return jsonpickle.encode(response)

    def subscribe(self, params):
        player = params.get("player")
        id_party = params.get("id_party")
        role = "villageois" if len(self.joueurs) > 0 else "loup"
        self.joueurs.append(Joueur(len(self.joueurs), role, 0, 0, "OK", 0))
        response = {
            "status": "OK",
            "response": {
                "role": role,
                "id_player": len(self.joueurs) - 1
            }
        }
        return jsonpickle.encode(response)

    def update_board(self, params):
        # Mettre à jour le plateau avec les nouveaux paramètres
        taille_x = params.get("taille_x")
        taille_y = params.get("taille_y")
        nb_obstacles = params.get("nb_obstacles")
        self.board = Plateau(taille_x, taille_y, nb_obstacles)
        response = {
            "status": "OK",
            "response": {
                "message": "Plateau mis à jour avec succès."
            }
        }
        return jsonpickle.encode(response)

    def run(self, action, params_str, client_target_ip, client_target_port):
        params = jsonpickle.decode(params_str)
        if action in self.actions:
            return self.actions[action](params)
        else:
            return jsonpickle.encode({"status": "KO", "response": "Unknown action"})

    def save_to_disk(self):
        # Méthode pour sauvegarder l'état du jeu sur le disque si nécessaire
        pass

    def close(self):
        # Méthode pour fermer proprement les ressources
        pass

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

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
        # message format: client_target_ip,client_target_port,action,params
        client_target_ip, client_target_port, action = request_split[0], request_split[1], request_split[2]
        app = App.get_instance()
        response = app.run(action.strip(), ','.join(request_split[3:]), client_target_ip, client_target_port)
        self.request.sendall(str(response).encode(encoding='utf-8'))
        app.save_to_disk()

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"Server running on {HOST}:{PORT}")
        server.serve_forever()

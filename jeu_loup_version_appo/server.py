# import socketserver
# import socket
# from Class_joueur import Joueur
# from Class_plateau import Plateau
# import json
# class App:
#     __instance = None

#     @classmethod
#     def get_instance(cls):
#         if cls.__instance is None:
#             cls.__instance = App()
#         return cls.__instance

#     def __init__(self):
#         self.actions = {
#             'party_status': self.party_status,
#             'gameboard_status': self.gameboard_status,
#             'move': self.move,
#             'list': self.list,
#             'subscribe': self.subscribe,
#         }
#         self.__reload_from_disk()
#         self.__init_game()
#         self.board = Plateau(10, 10, 5)
#         self.joueurs = []
#         self.clients = set()

#     def party_status(self, params):
#         # Exemple de réponse pour l'état de la partie
#         response = {
#             "status": "OK",
#             "response": {
#                 "party": {
#                     "id_party": 1,
#                     "id_player": len(self.joueurs),
#                     "started": True,
#                     "round_in_progress": 1,
#                     "move": {
#                         "next_position": {
#                             "row": 0,
#                             "col": 1
#                         }
#                     }
#                 }
#             }
#         }
#         return json.dumps(response)

#     def gameboard_status(self, params):
#         # Exemple de réponse pour l'état du plateau
#         response = {
#             "status": "OK",
#             "response": {
#                 "visible_cells": "010010000"  # Exemple de chaîne représentant le plateau
#             }
#         }

#     def move(self, params):
#         # Logique de déplacement à implémenter
#         response = {
#             "status": "OK",
#             "response": {
#                 "round_in_progress": 1,
#                 "move": {
#                     "next_position": {
#                         "row": int([0]),
#                         "col": int([1])
#                     }
#                 }
#             }
#         }

#     def list(self, params):
#         # Exemple de réponse pour la liste des parties
#         response = {
#             "status": "OK",
#             "response": {
#                 "id_parties": [1, 2, 3]
#             }
#         }

#     def subscribe(self, params):

#         new_joueur = Joueur(id=player_id, role="villageois", co_x=0, co_y=0, etat="actif", deplacement=0)
#         self.joueurs.append(new_joueur)

#         response = {
#             "status": "OK",
#             "response": {
#                 "role": "villageois",
#                 "id_player": player_id
#             }
#         }
#         return json.dumps(response)
    
#     def __del__(self):
#         self.db.close()

#     def run(self, action, params, client_target_ip, client_target_port):
#         self.clients.add((client_target_ip, int(client_target_port)))
#         return self.actions[action](params)

# class MyTCPHandler(socketserver.BaseRequestHandler):
#     def handle(self):
#         pieces = [b'']
#         total = 0
#         while b'\n' not in pieces[-1] and total < 10_000:
#             pieces.append(self.request.recv(2000))
#             total += len(pieces[-1])
#         self.data = b''.join(pieces)
#         print(f"Received from {self.client_address[0]}:")
#         request = self.data.decode("utf-8")
#         print(f'request: {request}')
#         request_split = request.split(',')

#         client_target_ip, client_target_port, action = request_split[0], request_split[1], request_split[2]
#         app = App.get_instance()
#         response = app.run(action.strip(), ','.join(request_split[3:]), client_target_ip, client_target_port)
#         self.request.sendall(str(response).encode(encoding='utf-8'))
#         app.save_to_disk()

# if __name__ == "__main__":
#     HOST, PORT = "localhost", 9999
#     with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
#         server.serve_forever()
import grpc
from concurrent import futures
import game_pb2
import game_pb2_grpc

class GameService(game_pb2_grpc.GameServiceServicer):
    def PartyStatus(self, request, context):
        response = game_pb2.PartyStatusResponse(
            status="OK",
            party=game_pb2.Party(
                id_party=1,
                id_player=2,
                started=True,
                round_in_progress=1,
                next_move=game_pb2.Move(row=0, col=1)
            )
        )
        return response

    def GameboardStatus(self, request, context):
        response = game_pb2.GameboardStatusResponse(
            status="OK",
            visible_cells="010010000"
        )
        return response

    def Move(self, request, context):
        response = game_pb2.MoveResponse(
            status="OK",
            next_position=game_pb2.Move(row=request.row, col=request.col)
        )
        return response

    def List(self, request, context):
        response = game_pb2.ListResponse(
            status="OK",
            id_parties=[1, 2, 3]
        )
        return response

    def Subscribe(self, request, context):
        response = game_pb2.SubscribeResponse(
            status="OK",
            role="villageois",
            id_player=request.player_id
        )
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_pb2_grpc.add_GameServiceServicer_to_server(GameService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

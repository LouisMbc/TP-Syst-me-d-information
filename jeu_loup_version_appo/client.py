import socket
import json

class Client:
    def __init__(self, client_host_ip='localhost', client_host_port=9999):
        self.host = client_host_ip
        self.port = client_host_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.actions = {
            "party_status": self.party_status,
            "gameboard_status": self.gameboard_status,
            "move": self.move,
            "list": self.list,
            "subscribe": self.subscribe
        }

    def send_request(self, request):
        self.client_socket.send(json.dumps(request).encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')
        return json.loads(response)

    def party_status(self):
        party_status_request = {"action": "party_status", "parameters": [{"id_player": 1}, {"id_party": 1}]}
        response = self.send_request(party_status_request)
        print(response)

    def gameboard_status(self):
        gameboard_status_request = {"action": "gameboard_status", "parameters": [{"id_party": 1}, {"id_player": 1}]}
        response = self.send_request(gameboard_status_request)
        print(response)

    def move(self):
        move_request = {"action": "move", "parameters": [{"id_party": 1}, {"id_player": 1}, {"move": "01"}]}
        response = self.send_request(move_request)
        print(response)

    def list(self):
        list_request = {"action": "list", "parameters": []}
        response = self.send_request(list_request)
        print(response)

    def subscribe(self):
        subscribe_request = {"action": "subscribe", "parameters": [{"player": "player1", "id_party": 1}]}
        response = self.send_request(subscribe_request)
        print(response)

    def close(self):
        self.client_socket.close()

if __name__ == "__main__":
    client = Client()
    # Exemple d'utilisation
    client.list()
    client.subscribe()
    client.party_status()
    client.gameboard_status()
    client.move()
    client.close()

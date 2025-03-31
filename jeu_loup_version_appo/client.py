# import tkinter as tk
# from tkinter import *
# import socket
# import socketserver
# from threading import Thread


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

#     def __send(self, message):
#         received = None
#         message_to_send = f'{self.__client_host_ip},{self.__client_host_port},{message}'
#         # Create a socket (SOCK_STREAM means a TCP socket)
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#             # Connect to server and send data
#             sock.connect((self.__host, self.__port))
#             sock.sendall(bytes(message_to_send, "utf-8"))
#             sock.sendall(b"\n")
#             # Receive data from the server and shut down
#             received = str(sock.recv(1024), "utf-8")
#         return received
    


# class HandlerNotification(socketserver.BaseRequestHandler):

#     def handle(self):
#         print('trigger notification')

# def wait_for_notification(client_port):
#     HOST, PORT = "localhost", client_port

#     # Create the server, binding to localhost on port 9999
#     with socketserver.TCPServer((HOST, PORT), HandlerNotification) as server:
#         # Activate the server; this will keep running until you
#         # interrupt the program with Ctrl-C
#         server.serve_forever()

# if __name__ == "__main__":
#     client_port = int(input('client port: '))
#     thread_notification = Thread(target=wait_for_notification, args=[client_port])
#     thread_notification.start()
#     client = Client('localhost', client_port)
#     client.run()
#     # useless for now
#     thread_notification.join()
import tkinter as tk
from tkinter import messagebox
import socket
import socketserver
import json

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
        self.create_widgets()

    def create_widgets(self):
        # Créer une interface simple pour interagir avec le client
        self.status_label = tk.Label(self.root, text="Statut du jeu:")
        self.status_label.pack()

        self.action_label = tk.Label(self.root, text="Action:")
        self.action_label.pack()

        self.action_entry = tk.Entry(self.root)
        self.action_entry.pack()

        self.send_button = tk.Button(self.root, text="Envoyer", command=self.send_action)
        self.send_button.pack()

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

class HandlerNotification(socketserver.BaseRequestHandler):
    def handle(self):
        print('Notification reçue')
        data = self.request.recv(1024).strip()
        print(f"Notification: {data.decode('utf-8')}")

def wait_for_notification(client_port):
    HOST, PORT = "localhost", client_port
    with socketserver.TCPServer((HOST, PORT), HandlerNotification) as server:
        server.serve_forever()

if __name__ == "__main__":
    client_port = int(input('client port: '))
    client = Client('localhost', client_port)
    client.run()

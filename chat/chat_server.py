# chat_server.py
import socket
import threading

clients = {}
rooms = {}

def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith('/join'):
                room_name = message.split()[1]
                if room_name not in rooms:
                    rooms[room_name] = []
                rooms[room_name].append(client_socket)
                clients[client_socket] = room_name
                client_socket.send(f"You have joined room: {room_name}".encode('utf-8'))
            elif message:
                room_name = clients[client_socket]
                for client in rooms[room_name]:
                    if client != client_socket:
                        client.send(message.encode('utf-8'))
        except:
            break

    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("Server started on port 5555")

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()

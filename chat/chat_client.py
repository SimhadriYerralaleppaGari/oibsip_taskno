# chat_client.py
import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

class ChatClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        self.root = tk.Tk()
        self.root.title("Chat Application")
        
        self.chat_area = scrolledtext.ScrolledText(self.root, state='disabled')
        self.chat_area.pack(padx=10, pady=10)

        self.message_input = tk.Entry(self.root)
        self.message_input.pack(padx=10, pady=10, fill=tk.X)
        self.message_input.bind("<Return>", self.send_message)

        self.username = simpledialog.askstring("Username", "Enter your username:")
        self.room_name = simpledialog.askstring("Chat Room", "Enter room name:")
        self.client_socket.send(f"/join {self.room_name}".encode('utf-8'))

        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def send_message(self, event=None):
        message = self.message_input.get()
        self.client_socket.send(f"{self.username}: {message}".encode('utf-8'))
        self.message_input.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(tk.END, message + "\n")
                    self.chat_area.config(state='disabled')
                    self.chat_area.yview(tk.END)
            except Exception as e:
                self.root.after(0, self.show_connection_error)
                break

    def show_connection_error(self):
        messagebox.showerror("Error", "Connection to server lost.")
        self.client_socket.close()
        self.root.quit()

    def on_closing(self):
        self.client_socket.close()
        self.root.quit()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 5555
    ChatClient(host, port)
    tk.mainloop()

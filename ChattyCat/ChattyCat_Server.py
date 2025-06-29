import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

HOST = '127.0.0.1'
PORT = 9999

class ChatServer:
    def __init__(self, root):
        #TCP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {} 
        self.root = root
        self.setup_gui()
        self.start_server()

    def setup_gui(self):
        self.root.title("Chat Server")
        self.root.geometry("500x400")
        
        # Log display
        self.log_area = scrolledtext.ScrolledText(self.root, height=15, width=50, state='disabled')
        self.log_area.pack(padx=10, pady=10)
        
        # Stop button
        tk.Button(self.root, text="Stop Server", command=self.stop_server).pack(pady=5)
        
        self.log("Server GUI initialized")

    def log(self, message):
        self.log_area.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.config(state='disabled')
        self.log_area.yview(tk.END)

    def start_server(self):
        try:
            #binds to localhost and port 9999
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen()
            self.log(f"Server listening on {HOST}:{PORT}")
            threading.Thread(target=self.accept_clients, daemon=True).start()
        except Exception as e:
            self.log(f"Server error: {e}")
    #runs in a thread for each client to handle messages
    def accept_clients(self):
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                self.clients[client_socket] = addr
                self.log(f"Connected to {addr}")
                threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()
            except:
                break
    
    #receives messages and logs them
    def handle_client(self, client_socket, addr):
        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if not msg or msg.lower() == 'quit':
                    self.log(f"Client {addr} disconnected")
                    break
                self.log(f"Client {addr}: {msg}")
                self.broadcast(f"Client {addr[1]}: {msg}", client_socket)
            except:
                break
        self.remove_client(client_socket)
    #broadcasts the message to all other clients
    def broadcast(self, msg, sender_socket):
        for client_socket in list(self.clients.keys()):
            if client_socket != sender_socket:
                try:
                    client_socket.send(msg.encode('utf-8'))
                except:
                    self.remove_client(client_socket)
    #clean-up if a client disconnects
    def remove_client(self, client_socket):
        if client_socket in self.clients:
            addr = self.clients.pop(client_socket)
            client_socket.close()
            self.log(f"Removed client {addr}")

    def stop_server(self):
        self.log("Shutting down server...")
        for client_socket in list(self.clients.keys()):
            self.remove_client(client_socket)
        self.server_socket.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    server = ChatServer(root)
    root.mainloop()
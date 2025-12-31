import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

HOST = '127.0.0.1'
PORT = 9999

class ChatClient:
    def __init__(self, root):
        #Again, TCP socket setup
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.root = root
        self.running = True
        self.setup_gui()
        self.connect_to_server()

    def setup_gui(self):
        self.root.title("Chat Client")
        self.root.geometry("500x400")
        
        # Chat display
        self.chat_area = scrolledtext.ScrolledText(self.root, height=15, width=50, state='disabled')
        self.chat_area.pack(padx=10, pady=10)
        
        # Message input
        self.msg_entry = tk.Entry(self.root, width=40)
        self.msg_entry.pack(side=tk.LEFT, padx=5)
        self.msg_entry.bind("<Return>", lambda event: self.send_message())
        
        # Send button
        tk.Button(self.root, text="Send", command=self.send_message).pack(side=tk.LEFT)
        
        # Quit button
        tk.Button(self.root, text="Quit", command=self.quit).pack(side=tk.LEFT, padx=5)
        
        self.log("Client GUI initialized")

    #shows all messages sent and received
    def log(self, message):
        self.chat_area.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    #starts a thread to continuosly receive messages
    def connect_to_server(self):
        try:
            self.client_socket.connect((HOST, PORT))
            self.log("Connected to server")
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.log(f"Connection error: {e}")

    #listens for incoming messages and dispalys them in the log
    def receive_messages(self):
        while self.running:
            try:
                msg = self.client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                self.log(msg)
            except:
                break
        self.log("Disconnected from server")

    #sends messages to the server
    def send_message(self):
        msg = self.msg_entry.get().strip()
        if msg:
            try:
                self.client_socket.send(msg.encode('utf-8'))
                self.log(f"You: {msg}")
                self.msg_entry.delete(0, tk.END)
                #one of the ways to  close the program (see line 83)
                if msg.lower() == 'quit':
                    self.quit()
            except:
                self.log("Failed to send message")

    def quit(self):
        self.running = False
        self.client_socket.send("quit".encode('utf-8'))
        self.client_socket.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
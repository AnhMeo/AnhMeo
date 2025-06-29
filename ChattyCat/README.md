# Overview
This is a project that pushed me to do a lot of research and learn how to put networking and programming
concepts I have learned into a real world application. The goal was to create a functional, user-friendly 
chat system that demonstrates core networking principles using Python.
To get this to work, follow these steps: 
1. Run the server FIRST: simply run the server in VSCode
2. Create a new terminal
3. use the CLI of the terminal to run the client: python .\ChattyCat_Client.py
4. The client will now be connected to the server. Repeat steps 2-3 to add additional clients. 
5. Use the client GUI windows to chat!


[Software Demo Video](https://youtu.be/WTS-si790U8)

# Network Communication

In this chat application, I am using a client/server architecture that allows for several clients to connect. 

I am using TCP through SOCK_STREAM, and I chose to use port 9999 as it is unassigned, so it is available for use here.

The  messages are in the utf-8 format. 

# Development Environment

This program was developed in VSCode

Language: Python

The following libraries were used: 
* Socket - for the networking and communication
* Tkinter - for the GUI
* Threading - for continued listening for messages and to allow multiple clients
* Datetime - for the timestamps on messages


# Useful Websites


* [Python - Socket](https://docs.python.org/3/library/socket.html)
* [Python - Tkinter](https://docs.python.org/3/library/tkinter.html)
* [Python - Threading](https://docs.python.org/3/library/threading.html)
* [Simple python chat application tutorial video](https://www.youtube.com/watch?v=Ar94t2XhKzM)
* [Python - Threading - Daemon](https://docs.python.org/3/library/threading.html#threading.Thread.daemon)
* [Python - Socket - SOCK_STREAM](https://docs.python.org/3/library/socket.html#socket.SOCK_STREAM)`

# Future Work


* Create a feature for the client that allows users to set their username
* Create a server feature that automatically assigns a color to the client names to easily differentiate who is talking
* Improve error handling and work on a reconnection feature
* Possible future feature: add support for cross-platform client connections (e.g., Windows, macOS, Linux)
# A3-371
A simple TCP-based file transfer application built in Python using socket programming.

Created by Wilson Tu (301598563) and Rushil Seghal (301576003)

Credits to ChatGPT for GUI elements, and Claude for debugging

# TCP File Transfer Application

## Description
This project implements a TCP-based file transfer system in Python using a client-server architecture. The client can select and send one or multiple files to the server over a socket connection. The server receives the files and saves them locally in a designated folder.

## Features
- TCP client-server communication
- Multiple file transfer in a single session
- Graphical user interface (GUI) for file selection
- File transfer progress display
- Automatic creation of a folder for received files

## Requirements
- Python 3.x
- No external libraries required (uses built-in modules: socket, os, tkinter)

## How to Run (Step-by-Step)

### 1. Start the Server
Open a terminal in the project folder and run:
python server.py

You should see:
[SERVER] Listening on 0.0.0.0:5001...

### 2. Run the Client
Open a new terminal and run:
python client.py

### 3. Send Files
1. Click "Add Files"
2. Select one or multiple files (hold Ctrl or Shift to select multiple)
3. Repeat to add more files if needed
4. Click "Send Files"

### 4. Output Location
All received files are saved in:
received_files/

Files are stored with their original filenames.

## Project Structure
```
project/
│── server.py
│── client.py
│── received_files/
│── README.md
```

## Limitations
- Supports only one client connection at a time
- No encryption or security for file transfer
- Does not support resuming interrupted transfers
- Assumes a stable network connection
- GUI is basic and not intended for large-scale use

## Notes
- The server must be started before running the client
- Default connection uses 127.0.0.1 (localhost)
- Works best when both client and server are on the same machine or network

## Demo Overview
This application demonstrates:
- Establishing a TCP connection
- Sending multiple files from client to server
- Receiving and storing files correctly on the server side


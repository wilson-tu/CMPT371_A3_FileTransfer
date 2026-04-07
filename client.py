import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Server connection settings
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5001

# Tracks the list of file paths the user has selected
selected_files = []

def choose_files(): # Open a file picker and add chosen files to the selection list
    global selected_files
    files = filedialog.askopenfilenames()
    if files:
        for f in files:
            if f not in selected_files:
                selected_files.append(f)
                file_listbox.insert(tk.END, os.path.basename(f))

def clear_files(): # Clear all selected files and reset the progress label
    global selected_files
    selected_files.clear()
    file_listbox.delete(0, tk.END)
    progress_label.config(text="Progress: 0")

def send_files(): # Connect to the server and send all selected files one by one
    global selected_files

    if not selected_files:
        messagebox.showerror("Error", "No files selected.")
        return

    try:
        # Establish a TCP connection to the server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_HOST, SERVER_PORT))

        for filepath in selected_files:
            filesize = os.path.getsize(filepath)
            filename = os.path.basename(filepath)

            # Send a header line with filename and size
            header = f"{filename}|{filesize}\n"
            client.sendall(header.encode())

            sent = 0

            # Read and send the file in 1 KB chunks
            with open(filepath, "rb") as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    client.sendall(data)
                    sent += len(data)

                    progress_label.config(
                        text=f"{filename}: {sent}/{filesize}"
                    )
                    root.update_idletasks()

        client.sendall(b"DONE\n") # Signal to the server that all files have been sent
        client.close()

        messagebox.showinfo("Success", "All files sent!")

        clear_files()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# --- GUI ---
root = tk.Tk()
root.title("File Transfer Client")
root.geometry("420x380")
root.configure(bg="#1e1e1e")

title = tk.Label(
    root,
    text="File Transfer Client",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="#1e1e1e"
)
title.pack(pady=10)

button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=5)

select_btn = tk.Button(button_frame, text="Add Files", command=choose_files, width=15)
select_btn.grid(row=0, column=0, padx=5)

clear_btn = tk.Button(button_frame, text="Clear List", command=clear_files, width=15)
clear_btn.grid(row=0, column=1, padx=5)

send_btn = tk.Button(root, text="Send Files", command=send_files, width=32)
send_btn.pack(pady=5)

# Scrollable list showing all the selected file names
frame = tk.Frame(root)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

file_listbox = tk.Listbox(
    frame,
    width=50,
    height=12,
    yscrollcommand=scrollbar.set
)
file_listbox.pack()

scrollbar.config(command=file_listbox.yview)

# Label that shows per-file transfer progress
progress_label = tk.Label(
    root,
    text="Progress: 0",
    fg="lightgreen",
    bg="#1e1e1e"
)
progress_label.pack(pady=10)

root.mainloop()
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        tkinter_Instance.quit()


def on_closing(event=None):
    my_msg.set("{quit}")
    send()

tkinter_Instance = tkinter.Tk()
tkinter_Instance.title("messenger")

messages_frame = tkinter.Frame(tkinter_Instance)

scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

my_msg = tkinter.StringVar()
entry_field = tkinter.Entry(tkinter_Instance,width=50, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(tkinter_Instance, text="отправить", command=send)
send_button.pack()

tkinter_Instance.protocol("WM_DELETE_WINDOW", on_closing)


HOST = '127.0.0.1'
PORT = 123
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()

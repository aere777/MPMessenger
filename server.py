#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s соединено" % client_address)
        client.send(bytes("Введите имя", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = '%s Успешно родился.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s вступил в переписку" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    try:
        while True:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, name + ": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                break
    except Exception as e:
        print(str(e))
    finally:
        del clients[client]
        broadcast(bytes("%s покинул переписку" % name, "utf8"))


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 123
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("ожидание соединения")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

from os import close
import socket
import facilities as fc
host = "localhost"
port = 50006
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
def manage_list(s):
    s.send(' '.encode())
    data=s.recv(2048)
    data=fc.bytes_to_list(data)
    for i in data:
        print(i)
    s.send(' '.encode())
while True:
    data = s.recv(1024).decode()
    if data == "#777":
        manage_list(s)
    elif data == "#111":
        data = input("inserisci qualcosa: ")
        s.send(data.encode())
        print(fc.bytes_to_list(s.recv(1024)))
        data = input("inserisci qualcosa: ")
        s.send(data.encode())
        print(s.recv(1024).decode())
        var = ""
        while var != "stop":
            var = input("inserire il campo che si vuole modificare, stop per uscire: ")
            s.send(var.encode())
    elif data == "#000":
        s.close()
        close(0)
    else:
        print(data)
        data = input("--> ")
        s.send(data.encode())
"""
while True:
    data = s.recv(1024)
    print(data.decode())
    testo = input("--> ")
    if testo == "Eliminare":
        s.send(testo.encode())
        print(s.recv(1024).decode())
        testo = input("--> ").encode()
        s.send(testo) #<-- tabella
        lista = s.recv(1024)
        print(fc.bytes_to_list(lista))
        testo = input("inserire qualcosa per continuare: ").encode()
        s.send(testo)
        print(s.recv(1024).decode())
        testo = input("--> ").encode()
        s.send(testo)
        break
    elif testo == "Modificare":
        s.send(testo.encode())
        print(s.recv(1024).decode())
        testo = input("--> ")
        s.send(testo.encode())
        if testo == '1':
            lista = s.recv(1024)
            print(fc.bytes_to_list(lista))
            testo = input("inserire qualosa per continuare: ").encode()
            s.send(testo)
            print(s.recv(1024).decode())
            testo = input("--> ").encode()
            s.send(testo)
            # ora c'è l'inserimento dei campi nel dizionario
            campo = ""
            while campo != "inserisci: età":
                print(s.recv(1024).decode())
                testo = input("--> ")
                s.send(testo.encode())
            break
        elif testo == '2':
            lista = s.recv(1024)
            print(fc.bytes_to_list(lista))
            testo = input("inserire qualosa per continuare: ").encode()
            s.send(testo)
            print(s.recv(1024).decode())
            testo = input("--> ").encode()
            s.send(testo)
            # ora c'è l'inserimento dei campi nel dizionario
            campo = ""
            while campo != "insersci: cod_dipendente":
                print(s.recv(1024).decode())
                testo = input("--> ")
                s.send(testo.encode())
            break
    elif testo == "Leggere":
        s.send(testo.encode())
        print(s.recv(1024).decode())
        testo = input("--> ")
        s.send(testo.encode())
        lista = s.recv(1024)
        print(fc.bytes_to_list(lista))
    elif testo == "Creare":
        s.send(testo.encode())
        print(s.recv(1024).decode())
        testo = input("--> ")
        s.send(testo.encode())
        tmp = ""
        while tmp != "fine":
            tmp = s.recv(1024).decode()
            print(tmp)
            testo = input("--> ")
            s.send(testo.encode())
    elif testo == "Esci":
        s.close()
    s.send(testo.encode())
s.close()
"""
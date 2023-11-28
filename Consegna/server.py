from os import close
import socket
import mysql.connector 
import facilities as fc
from fpdf import FPDF
host_db = "localhost"
user_db = "root"
conns = mysql.connector.connect(
        host=host_db, #127.0.0.1
        user=user_db,
        password="",
        database="5B_TEPSIT",
        port=3306 
        )
def send_a_list(data,conn):
    conn.send('#777'.encode())
    conn.recv(1024)
    data = fc.list_to_bytes(data)
    conn.send(data)
    conn.recv(1024)


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Report di Lista', 0, 1, 'C')

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)


def generate_pdf_report(my_list, filename):
    pdf = PDF()
    pdf.add_page()

    pdf.chapter_body('STAMPA RISULTATO QUERY:')
    for item in my_list:
        pdf.chapter_body(f'- {item}')
    try:
        pdf.output(filename)
    except Exception as e:
        print(f"Errore nel salvataggio: {e}")

def scelta_campi(tabella,conn,cur):
    if tabella == 1:
        cur.execute("SELECT * FROM dipendenti")
    elif tabella == 2:
        cur.execute("SELECT * FROM zone_di_lavoro")
    #cur.fetchall()
    field_names = [i[0] for i in cur.description]
    print(field_names)
    conn.send("#111".encode())
    tmp = conn.recv(1024)
    conn.send(fc.list_to_bytes(field_names)) #fare for nel client
    tmp = conn.recv(1024)
    lista_campi = []
    conn.send("scigliere il/i campi da modificare".encode())
    d = ""
    while d != "stop":
        d = conn.recv(1024).decode()
        if d != "stop":
            lista_campi.append(d)
    return lista_campi



password = "pw1234"
host = "localhost"
port = 50006
campi = ('id','nome','cognome','posizione_lavorativa','data_assunzione','indirizzo','eta')
dipendenti = dict.fromkeys(campi)
campi2 = ('id_zona','nome_zona','numero_clienti','cod_dipendente')
zone_di_lavoro = dict.fromkeys(campi2)
def db_get(tabella,conn,conns_l):
    cur = conns_l.cursor()

    # si chiama una funzione di libreria passando i parametri di ricerca dell'utente. esempio controlla_caratteri(nome)
    if tabella == '1':
        query = "SELECT * FROM dipendenti"
        campi = ['id','nome','cognome','posizione_lavorativa','data_assunzione','indirizzo','eta']
    elif tabella == '2':
        campi = ['id_zona','nome_zona','numero_clienti','cod_dipendente']
        query = "SELECT * FROM zone_di_lavoro"
    cur.execute(query)
    dati = cur.fetchall()
    #conn.send("inserire qualcosa per continuare: ")
    send_a_list(dati,conn)
    conn.send("Stampare un report?(s/n)".encode())
    risp = conn.recv(1024).decode()
    conn.send("inserire il nome del file: ".encode())
    nome_f = conn.recv(1024).decode()
    if risp == "s" or risp == "S":
        try:
            #generate_pdf_report(dati, r'Y:\TEPSIT\esercizio_db\report.pdf') #<-- si specifica il percorso nel quale si vuole salvarlo
            generate_pdf_report(dati, f'/home/lorenzo/Desktop/5°B/TEPSIT/esercizio_db/Consegna/Report/{nome_f}.pdf')
        except Exception as e:
            conn.send(f"Errore nella stampa del report: {e}".encode())
        conn.send("stampa del report effettuata correttamente.".encode())

def db_get_par(tabella,parametri,conns_l):


    cur = conns_l.cursor()

    # si chiama una funzione di libreria passando i parametri di ricerca dell'utente. esempio controlla_caratteri(nome)
    clausole = ""
    for key,value in parametri.items():
        clausole += f"and {key} = '{value}' "
    

    if tabella == "1":
        query = f"SELECT * FROM dipendenti where 1=1 {clausole}"
    elif tabella == "2":
        query = f"SELECT * FROM zone di lavoro where 1=1 {clausole}"
    print(query)
    cur.execute(query)
    dati = cur.fetchall()
    print(dati)
    return dati
def crea(tabella,conn,conns_l):
    cur = conns_l.cursor()

    # si chiama una funzione di libreria passando i parametri di ricerca dell'utente. esempio controlla_caratteri(nome)
    if tabella == '1':
        conn.send("inserisci: nome".encode())
        dipendenti["nome"] = conn.recv(1024).decode()
        conn.send("inserisci: cognome".encode())
        dipendenti["cognome"] = conn.recv(1024).decode()
        conn.send("inserisci: posizione lavorativa".encode())
        dipendenti["posizione_lavorativa"] = conn.recv(1024).decode()
        conn.send("inserisci: data assunzione".encode())
        dipendenti["data_assunzione"] = conn.recv(1024).decode()
        conn.send("inserisci: indirizzo".encode())
        dipendenti["indirizzo"] = conn.recv(1024).decode()
        conn.send("inserisci: età".encode())
        dipendenti["eta"] = conn.recv(1024).decode()
        conn.send("fine".encode())
        try:
            query = "INSERT INTO dipendenti (nome, cognome, posizione_lavorativa, data_assunzione, indirizzo, eta) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (dipendenti["nome"], dipendenti["cognome"], dipendenti["posizione_lavorativa"], dipendenti["data_assunzione"], dipendenti["indirizzo"], dipendenti["eta"])
            cur.execute(query,values)
        except mysql.connector.Error as err:
            conn.send(f"errore nell'esecuzione della query: {err}")
    elif tabella == '2':
        conn.send("inserisci: nome_zona".encode())
        zone_di_lavoro["nome_zona"] = conn.recv(1024).decode()
        conn.send("inserisci: numero_clienti".encode())
        zone_di_lavoro["numero_clienti"] = conn.recv(1024).decode()
        conn.send("insersci: cod_dipendente".encode())
        zone_di_lavoro["cod_dipendente"] = conn.recv(1024).decode()
        conn.send("fine".encode())
        query = "INSERT INTO zone_di_lavoro (nome_zona, numero_clienti, cod_dipendente) VALUES (%s,%s,%s)"
        values = (zone_di_lavoro['nome_zona'],zone_di_lavoro['numero_clienti'],zone_di_lavoro['cod_dipendente'])
        cur.execute(query,values)
    conns.commit()
def elimina(tabella,conn,conns_l):
    cur = conns_l.cursor()
    if tabella == '1': 
        query = "select * from dipendenti"
        cur.execute(query)
        dati = cur.fetchall()
        send_a_list(dati,conn)
        #tmp = conn.recv(1024)
        conn.send(f"sciegliere l'id della persona da eliminare:".encode())
        id_pers = conn.recv(1024).decode()
        query = f"delete from dipendenti where id = {id_pers}"
    elif tabella == '2':
        query = "select * from zone_di_lavoro"
        cur.execute(query)
        dati = cur.fetchall()
        send_a_list(dati,conn)
        #tmp = conn.recv(1024)
        conn.send("sciegliere l'id della zona di lavoro da eliminare:".encode())
        id_zona_di_l = conn.recv(1024).decode()
        query = f"delete from zone_di_lavoro where id_zona = {id_zona_di_l}"
    cur.execute(query)
    conns.commit()
def modifica(tabella,conn,conns_l):
    cur = conns_l.cursor()
    if tabella == '1':
        query = "SELECT * FROM dipendenti"
        cur.execute(query)
        dati = cur.fetchall()
        send_a_list(dati,conn)
        #tmp = conn.recv(1024)
        conn.send("scigliere l'istanza da modificare: ".encode())
        id_istanza = conn.recv(1024).decode()
        lista_campi = scelta_campi(tabella,conn,cur)

        """
        conn.send("inserisci: nome".encode())
        dipendenti["nome"] = conn.recv(1024).decode()
        conn.send("inserisci: cognome".encode())
        dipendenti["cognome"] = conn.recv(1024).decode()
        conn.send("inserisci: posizione lavorativa".encode())
        dipendenti["posizione_lavorativa"] = conn.recv(1024).decode()
        conn.send("inserisci: data assunzione".encode())
        dipendenti["data_assunzione"] = conn.recv(1024).decode()
        conn.send("inserisci: indirizzo".encode())
        dipendenti["indirizzo"] = conn.recv(1024).decode()
        conn.send("inserisci: età".encode())
        dipendenti["eta"] = conn.recv(1024).decode()
        """
        dipendenti_l = []
        for i in lista_campi:
            conn.send(f"campo: {i}".encode())
            dipendenti_l.append(conn.recv(1024).decode())
        n = 0
        #query = "UPDATE dipendenti SET nome = %s, cognome = %s, posizione_lavorativa = %s, data_assunzione = %s, indirizzo = %s, eta = %s WHERE id = %s"
        print(dipendenti_l)
        print(lista_campi)
        for i in lista_campi:
            query = f"UPDATE dipendenti SET {i} = '{dipendenti_l[n]}' WHERE id = {id_istanza}"
            cur.execute(query)
            n += 1
        conns.commit()
        #values = (dipendenti["nome"],dipendenti["cognome"],dipendenti["posizione_lavorativa"],dipendenti["data_assunzione"],dipendenti["indirizzo"],dipendenti["eta"],id_istanza)
    if tabella  == '2':
        query = "SELECT * FROM zone_di_lavoro"
        cur.execute(query)
        dati = cur.fetchall()
        send_a_list(dati,conn)
        #tmp = conn.recv(1024)
        conn.send("scigliere l'istanza da modificare: ".encode())
        id_istanza = conn.recv(1024).decode()
        lista_campi = scelta_campi(tabella,conn,cur)
        """
        conn.send("inserisci: nome_zona".encode())
        zone_di_lavoro["nome_zona"] = conn.recv(1024).decode()
        conn.send("inserisci: numero_clienti".encode())
        zone_di_lavoro["numero_clienti"] = conn.recv(1024).decode()
        conn.send("insersci: cod_dipendente".encode())
        zone_di_lavoro["cod_dipendente"] = conn.recv(1024).decode()
        query = "UPDATE zone_di_lavoro SET nome_zona = %s, numero_clienti = %s, cod_dipendente = %s WHERE id_zona = %s"
        values = (zone_di_lavoro["nome_zona"],zone_di_lavoro["numero_clienti"],zone_di_lavoro["cod_dipendente"],id_istanza)
        """
        zone_di_lavoro_l = []
        for i in lista_campi:
            conn.send(f"campo: {i}".encode())
            zone_di_lavoro_l.append(conn.recv(1024).decode())
        n = 0
        for i in lista_campi:
            query = f"UPDATE zone_di_lavoro SET {i} = '{zone_di_lavoro_l[n]}' WHERE id_zona = {id_istanza}"
            cur.execute(query)
            n += 1
    conns.commit()


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))

s.listen(1)
print("server in ascolto...")
conn,addr = s.accept()
n = 3
i = 0
while n>0 or i<3:
    conn.send("inserire la password: ".encode())
    pw = conn.recv(1024).decode()
    if pw == password:
        conn.send("password corretta, premi un tasto per continuare".encode())
        break
    else:
        conn.send(f"password errata, ancora {n} tentativi".encode())
        n -= 1
    i += 1
if n<1:
    conn.close()
else: 
    tmp = conn.recv(1024)
    while True:
        conn.send("menu: \n1. Creare \n2. Leggere \n3. Modificare \n4. Eliminare \n5. Esci".encode())
        dato = conn.recv(1024).decode() #<-- qui c'è la risposta
        if dato == "1":
            conn.send("su quale tabella (1. dipendenti, 2. zone di lavoro): ".encode())
            tabella = conn.recv(1024).decode()
            crea(tabella,conn,conns)
        elif dato == "2":
            conn.send("su quale tabella (1. dipendenti, 2. zone di lavoro): ".encode())
            tabella = conn.recv(1024).decode()
            query = db_get(tabella,conn,conns)
        elif dato == "3":
            conn.send("su quale tabella (1. dipendenti, 2. zone di lavoro): ".encode())
            tabella = conn.recv(1024).decode()
            modifica(tabella,conn,conns)
        elif dato == "4":
            conn.send("su quale tabella (1. dipendenti, 2. zone di lavoro): ".encode())
            tabella = conn.recv(1024).decode()
            elimina(tabella,conn,conns)
        elif dato == "5":
            conn.send("#000".encode())
            conn.close()
            close(0)
    #tmp = conn.recv(1024)
    #conn.send("inserire qualcosa per continuare: ".encode())
    #risp = conn.recv(1024).decode()
    #conn.send("lista".encode())
    #risp = conn.recv(1024).decode()
    #ris_query = db_get()
    #print(ris_query)
    #byt = fc.list_to_bytes(ris_query)
    #conn.send(byt)
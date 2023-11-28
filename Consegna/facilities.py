import pickle
import socket


def string_to_bytes(data):
    """
    metodo per trasformare le stringhe in bytes prima di inviarle con l'utilizzo del metodo send
    della libreria socket
    """
    if not isinstance(data, str):
        raise Exception("devi passare una stringa alla funzione string_to_bytes")

    return data.encode()


def bytes_to_string(data):
    """
    metodo per trasformare i bytes in stringhe una volta ricevute con l'utilizzo del metodo recv
    della libreria socket
    """
    if not isinstance(data, bytes):
        raise Exception("devi passare dei bytes alla funzione bytes_to_string")

    return data.decode()


def list_to_bytes(data):
    """
    metodo per trasformare le liste in bytes prima di inviarle con l'utilizzo del metodo send
    della libreria socket
    """
    if not isinstance(data, list):
        raise Exception("devi passare una lista alla funzione list_to_bytes")
    list_converted = pickle.dumps(data)
    return list_converted



def bytes_to_list(data):
    """
    metodo per trasformare i bytes in liste una volta ricevute con l'utilizzo del metodo recv
    della libreria socket
    """
    if not isinstance(data, bytes):
        raise Exception("devi passare dei bytes alla funzione bytes_to_list")

    return pickle.loads(data)


def dict_to_bytes(data):
    """
    metodo per trasformare dizionari in bytes prima di inviarli con l'utilizzo del metodo send
    della libreria socket
    """
    if not isinstance(data, dict):
        raise Exception("devi passare una lista alla funzione dict_to_bytes")
    list_converted = pickle.dumps(data, -1)
    return list_converted


def bytes_to_dict(data):
    """
    metodo per trasformare i bytes in dizionari una volta ricevuti con l'utilizzo del metodo recv
    della libreria socket
    """
    if not isinstance(data, bytes):
        raise Exception("devi passare dei bytes alla funzione bytes_to_dict")

    return pickle.loads(data)


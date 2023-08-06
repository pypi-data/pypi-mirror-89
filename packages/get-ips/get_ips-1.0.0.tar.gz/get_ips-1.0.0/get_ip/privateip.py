def private():
    import socket
    priv_ip = socket.gethostbyname(socket.gethostname())
    return priv_ip
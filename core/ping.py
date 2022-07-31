import socket

def myping(host: str, port: int):
    if('http://' in host):
        host = host.replace('http://', '')
    if('https://' in host):
        host = host.replace('https://', '')
    try:
        socket.setdefaulttimeout(3)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, port)
        s.connect(server_address)
    except OSError as error:
        return False
    else:
        s.close()
        return True
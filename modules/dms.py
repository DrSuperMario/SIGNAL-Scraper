import socket
import selectors

from connection.var import Constants

sel = selectors.DefaultSelector()

_host = Constants.FALLBACK_ADDR.value
_port = Constants.FALLBACK_PORT.value



def send_ping(host=_host, port=_port):
    server_addr = (host, port) 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = b"Keepalive"
    sel.register(sock, events, data=data)



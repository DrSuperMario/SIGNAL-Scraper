import socket

from connection.var import Constants


_host = Constants.FALLBACK_ADDR.value
_port = Constants.FALLBACK_PORT.value



def send_ping(host=_host, port=_port):
    server_addr = (host, port) 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(1)
    sock.connect(server_addr)
    message = "Keepalive"
    sock.send(message.encode())
    sock.close()
    
if __name__=="__main__":
    send_ping()


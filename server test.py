import socket
from basic_socket import *

server = BasicSocket()
server.sock.bind(("localhost", 4999))
server.sock.listen(5)

pingMessage = "this is a reply from the server, your message was received successfully!"
while True:
    (clientsocket, address) = server.sock.accept()
    client = BasicSocket(clientsocket)
    del clientsocket
    print("connected, waiting to receive data...")
    recvData = client.receiveUTF8()
    print(f"client message: \"{recvData}\"")
    print(f"sending \"{pingMessage}\"")
    client.sendUTF8(pingMessage)
    client.sock.close()
    
import socket
from basic_socket import *

server = BasicSocket()
server.sock.bind(("localhost", 7777))
server.sock.listen(5)

pingMessage = "this is a reply from the server, your message was recieved successfully!"
while True:
    (clientsocket, address) = server.sock.accept()
    client = BasicSocket(clientsocket)
    del clientsocket
    print("connected, waiting for a recieveAll()...")
    recvData = client.recieveUTF8()
    print(f"client message: \"{recvData}\"")
    print(f"sending \"{pingMessage}\"")
    client.sendUTF8(pingMessage)

    break
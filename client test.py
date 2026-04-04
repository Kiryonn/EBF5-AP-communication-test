import socket
from basic_socket import *

client = BasicSocket()
client.connect("localhost", 4999)
client.sendUTF8("4 byte length and then UTF-8 text string packet send from the client.")
serverMessage = client.receiveUTF8()
print(f"server reply: \"{serverMessage}\"")
# client.sock.shutdown(socket.SHUT_WR)
client.sock.close()
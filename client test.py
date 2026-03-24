import socket
from basic_socket import *

client = BasicSocket()
client.connect("localhost", 7777)
client.sendUTF8("a different length message wouldn't have worked earlier!")
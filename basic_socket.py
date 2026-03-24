import socket
import struct
# bytes 1-4 are an unsigned 32 bit length. maybe a bit overkill, but i think it's fine.



# this is broken and im gonna take a break.
class BasicSocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def sendUTF8(self, msg):
        lengthBytesSent = 0
        charsSend = 0
        textLength = len(bytes(msg, encoding="utf-8"))
        print(bytes(str(msg), encoding="utf-8"), textLength)
        lengthBytes = bytes(socket.htonl(textLength))
        print(lengthBytes)
        while lengthBytesSent < 4:
            sent = self.sock.send(lengthBytes[lengthBytesSent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            lengthBytesSent += sent
            print(lengthBytesSent, lengthBytes[lengthBytesSent:])
        print(len(msg), charsSend < len(msg))
        while charsSend < len(msg):
            print(charsSend < len(msg), bytes(msg[charsSend:], encoding="utf-8"))
            sent = self.sock.send(bytes(msg[charsSend:], encoding="utf-8"))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            charsSend += sent
            print(charsSend, bytes(msg[charsSend:], encoding="utf-8"))
        print("finished sending")

    def recieveUTF8(self):
        chunks = []
        lengthBytes:bytes = b""
        bytesRecieved = 0
        textLength = 0
        while bytesRecieved < 4:
            chunk = self.sock.recv(4-bytesRecieved)
            print(chunk)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            lengthBytes.__add__(chunk)
            bytesRecieved += len(chunk)

        textLength = int.from_bytes(lengthBytes, "big", signed=True)
        print(textLength, bytesRecieved, textLength + 4)
        while bytesRecieved < textLength + 4:
            chunks = [] # we don't want the length bytes to be interpreted as part of the string
            chunk = self.sock.recv(min(textLength - bytesRecieved, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytesRecieved += len(chunk)
        print("finished recieving")
        return str(b''.join(chunks), encoding="utf-8")
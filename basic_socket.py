import socket
# bytes 1-4 are an unsigned 32 bit length. maybe a bit overkill, but i think it's fine.


class BasicSocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def sendUTF8(self, msg:str):
        lengthBytesSent = 0
        charsSend = 0
        textLength = len(msg.encode("utf-8"))
        print(textLength)
        lengthBytes = textLength.to_bytes(4, "big", signed=False)
        print(lengthBytes)
        while lengthBytesSent < 4:
            sent = self.sock.send(lengthBytes[lengthBytesSent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            lengthBytesSent += sent
            print(lengthBytesSent, lengthBytes[lengthBytesSent:])
        print(len(msg), charsSend < len(msg))
        while charsSend < len(msg):
            print(charsSend < len(msg), msg[charsSend:].encode("utf-8"))
            sent = self.sock.send(msg[charsSend:].encode("utf-8"))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            charsSend += sent
            print(charsSend, msg[charsSend:].encode("utf-8"))
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
            lengthBytes += chunk
            bytesRecieved += len(chunk)
        print(lengthBytes)
        textLength = int.from_bytes(lengthBytes, "big", signed=False)
        print(textLength, bytesRecieved, textLength - 4)
        chunks = [] # we don't want the length bytes to be interpreted as part of the string
        while bytesRecieved-4 < textLength:
            chunk = self.sock.recv(min(textLength - bytesRecieved + 4, 2048))
            print(chunk)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytesRecieved += len(chunk)
        print("finished recieving")
        return str(b''.join(chunks), encoding="utf-8")
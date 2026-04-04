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
        lengthBytes = textLength.to_bytes(4, "big", signed=False)
        while lengthBytesSent < 4:
            sent = self.sock.send(lengthBytes[lengthBytesSent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            lengthBytesSent += sent
        while charsSend < len(msg):
            sent = self.sock.send(msg[charsSend:].encode("utf-8"))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            charsSend += sent

    def receiveUTF8(self):
        chunks = []
        lengthBytes:bytes = b""
        bytesreceived = 0
        textLength = 0
        while bytesreceived < 4:
            chunk = self.sock.recv(4-bytesreceived)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            lengthBytes += chunk
            bytesreceived += len(chunk)
        textLength = int.from_bytes(lengthBytes, "big", signed=False)
        chunks = [] # we don't want the length bytes to be interpreted as part of the string
        while bytesreceived-4 < textLength:
            chunk = self.sock.recv(min(textLength - bytesreceived + 4, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytesreceived += len(chunk)
        return str(b''.join(chunks), encoding="utf-8")
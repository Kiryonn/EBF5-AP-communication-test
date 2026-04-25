from socket import socket as Socket, AF_INET, SOCK_STREAM, SHUT_RDWR
# bytes 1-4 are an unsigned 32 bit length. maybe a bit overkill, but i think it's fine.


class SocketConnectionBrokenError(RuntimeError):
    def __init__(self, *args):
        super().__init__("socket connection broken", *args)


class BasicSocket:
    def __init__(self, sock: Socket = None, *, timeout: float = -1):
        self.sock: Socket = Socket(AF_INET, SOCK_STREAM) if sock is None else sock
        if timeout >= 0:
            self.sock.settimeout(timeout)

    def connect(self, host, port: int):
        self.sock.connect((host, port))

    def close(self):
        # https://docs.python.org/3/howto/sockets.html#disconnecting
        self.sock.shutdown(SHUT_RDWR)
        self.sock.close()

    # ----- helpers -----

    def _send_all(self, data: bytes):
        """Sends bytes using the socket connection

        Args:
            data (bytes): the utf-8 message in bytes form

        Raises:
            SocketConnectionBrokenError: socket connection is broken/interrupted
        """
        view = memoryview(data)  # zero-copy when slicing bellow
        total = 0
        while total < len(view):
            sent = self.sock.send(view[total:])
            if sent == 0:
                raise SocketConnectionBrokenError()
            total += sent

    def _recv_exact(self, n: int) -> bytes:
        """Attempt to receive an exact number of bytes

        Args:
            n (int): the number of bytes awaited

        Raises:
            SocketConnectionBrokenError: socket connection is broken/interrupted

        Returns:
            bytes: the bytes received
        """
        buf = bytearray(n)
        view = memoryview(buf)  # zero-copy when slicing bellow
        total = 0
        while total < n:
            chunk = self.sock.recv_into(view[total:])
            if chunk == 0:
                raise SocketConnectionBrokenError()
            total += chunk
        return bytes(buf)

    # ----- protocol -----

    def send_utf8(self, msg: str) -> None:
        data = msg.encode("utf-8")
        header = len(data).to_bytes(4, "big", signed=False)
        self._send_all(header)
        self._send_all(data)

    def receive_utf8(self) -> str:
        header = self._recv_exact(4)
        length = int.from_bytes(header, "big", signed=False)
        data = self._recv_exact(length)
        return data.decode("utf-8")

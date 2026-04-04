# EBF5 AP communication test
We're probably gonna have the actual client repository somewhere else (we might not even end up using python!), this is just a quick and simple thing i made to test my UTF-8 sending and receiving with the game.  
  
also the code here is based on this: https://docs.python.org/3/howto/sockets.html
# Format used:
4 byte (32 bit) unsigned length, and then raw UTF-8 bytes that fill that length.

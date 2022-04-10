import socket

HEADERSIZE = 10

def connect(host, port=1234):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    return s

def get_message(s):
    new_msg = True
    full_msg = ''
    while True:
        msg = s.recv(16)
        if new_msg:
            if msg==b'':
                return None
            print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
            
        full_msg += msg.decode("utf-8")
        
        if len(full_msg)-HEADERSIZE == msglen:
            print("Full msg recived")
            return full_msg[HEADERSIZE:]
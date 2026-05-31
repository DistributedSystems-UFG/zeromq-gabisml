import multiprocessing #-
import zmq, sys #-
from time import sleep #-

SERVER_IP = "44.202.253.173" #- altere para o IP da maquina servidora

def server():
  context = zmq.Context()
  socket  = context.socket(zmq.REP)       # create reply socket
  socket.bind("tcp://*:12345")            # bind socket to address

  while True:
    message = socket.recv().decode()      # wait for incoming message
    parts   = message.strip().split(" ", 1)
    cmd     = parts[0].upper()
    arg     = parts[1] if len(parts) > 1 else ""

    if   cmd == "UPPER":   reply = arg.upper()        # new: uppercase
    elif cmd == "LOWER":   reply = arg.lower()        # new: lowercase
    elif cmd == "REVERSE": reply = arg[::-1]          # new: reverse string
    elif cmd == "COUNT":   reply = str(len(arg))      # new: char count
    elif cmd == "STOP":    reply = "STOPPING"
    else:                  reply = message + "*"

    socket.send(reply.encode())           # send reply (encoded)
    if cmd == "STOP":
      break                               # break out of loop and end

def client(host="localhost"):
  context = zmq.Context()
  socket  = context.socket(zmq.REQ)      # create request socket

  socket.connect(f"tcp://{host}:12345")  # connect to server
  for cmd in ["UPPER hello world", "LOWER ZEROMQ", "REVERSE python", "COUNT sistemas distribuidos", "STOP"]:
    socket.send(cmd.encode())            # send message
    message = socket.recv()              # block until response
    print(f"[CLIENT] '{cmd}' -> '{message.decode()}'")

#-
if __name__ == "__main__": #-
  if len(sys.argv) > 1: #-
    if sys.argv[1] == "server": server() #- run only server (AWS)
    elif sys.argv[1] == "client": client(sys.argv[2] if len(sys.argv) > 2 else SERVER_IP) #- run only client (AWS)
  else: #-
    s = multiprocessing.Process(target=server) #-
    c = multiprocessing.Process(target=client, args=("localhost",)) #-
    s.start() #-
    sleep(2) #-
    c.start() #-
    c.join() #-
    s.join() #-

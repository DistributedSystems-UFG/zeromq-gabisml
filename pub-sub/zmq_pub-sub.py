import multiprocessing
import zmq, time, sys, random

PUBLISHER_IP = "44.202.253.173" # altere para o IP da maquina publisher

def server():
  context = zmq.Context()         
  socket = context.socket(zmq.PUB)          # create a publisher socket
  socket.bind("tcp://*:12345")              # bind socket to the address
  tick = 0
  while True:
    tick += 1
    time.sleep(2)                           # publish every 2 seconds
    t = "TIME " + time.asctime()
    socket.send(t.encode())                 # publish the current time

    if tick % 2 == 0:                       # new: publish WEATHER every 2 cycles
      w = f"WEATHER temp={random.randint(20,38)}C umidade={random.randint(40,95)}%"
      socket.send(w.encode())

    if tick % 5 == 0:                       # new: publish NEWS every 5 cycles
      socket.send(b"NEWS ZeroMQ pub-sub funcionando com multiplos topicos")

def client(host="localhost", topic="TIME"):
  context = zmq.Context()
  socket = context.socket(zmq.SUB)          # create a subscriber socket
  socket.connect(f"tcp://{host}:12345")     # connect to the server
  socket.setsockopt(zmq.SUBSCRIBE, topic.encode()) # subscribe to topic

  for i in range(5):      # Five iterations
    msg = socket.recv()   # receive a message related to subscription 
    print(msg.decode())   # print the result      
#-
if __name__ == "__main__": #-
  if len(sys.argv) > 1: #-
    if sys.argv[1] == "server": server() #- run only publisher (AWS)
    elif sys.argv[1] == "client": #- run only subscriber (AWS)
      host  = sys.argv[2] if len(sys.argv) > 2 else PUBLISHER_IP #-
      topic = sys.argv[3] if len(sys.argv) > 3 else "TIME" #-
      client(host, topic) #-
  else: #-
    s = multiprocessing.Process(target=server) #-
    c = multiprocessing.Process(target=client, args=("localhost", "TIME")) #-
    s.start() #-
    time.sleep(2) #-
    c.start() #-
    c.join() #-
    s.terminate() #-

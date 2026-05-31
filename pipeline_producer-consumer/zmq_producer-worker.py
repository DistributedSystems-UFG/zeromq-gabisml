import multiprocessing #-
import zmq, time, pickle, sys, random #-

PORT_P = "5678"  
PORT_C = "5679"  
def producer():
  context = zmq.Context()              
  socket  = context.socket(zmq.PUSH)      # create a push socket
  socket.bind("tcp://127.0.0.1:" + PORT_P) # bind socket to address
  time.sleep(1)

  task_id = 0
  while True:
    task_id += 1
    task = {"id": task_id, "valor": random.randint(1, 100), "prioridade": random.choice(["ALTA","MEDIA","BAIXA"])}
    print("Produced task", task["id"], "valor", format(task["valor"],'03d')) #-
    socket.send(pickle.dumps(task))
    time.sleep(task["valor"] / 100)       

def filtro():
  context = zmq.Context()
  r = context.socket(zmq.PULL)
  r.connect("tcp://127.0.0.1:" + PORT_P) # pull from producer
  p = context.socket(zmq.PUSH)
  p.bind("tcp://127.0.0.1:" + PORT_C)    # push to consumer

  while True:
    task = pickle.loads(r.recv())
    if task["valor"] < 10:               # discard low-value tasks
      continue
    if task["prioridade"] == "ALTA":
      task["valor"] *= 2; task["boost"] = True
    else:
      task["boost"] = False
    task["processado_por"] = "filter"
    print(f"Filter forwarded task {task['id']:03d} valor={task['valor']:03d} boost={task['boost']}") #-
    p.send(pickle.dumps(task))

def consumer(filter_host="127.0.0.1"):
  context = zmq.Context()
  socket  = context.socket(zmq.PULL)     # create a pull socket
  socket.connect("tcp://" + filter_host + ":" + PORT_C) # connect to filter

  total = 0
  while True:
    task  = pickle.loads(socket.recv())  # receive work from filter
    total += 1
    print(f"Consumer got task {task['id']:03d} valor={task['valor']:03d} boost={task['boost']} (total={total})") #-
    time.sleep(task["valor"] * 0.01)     # pretend to work

if __name__ == "__main__": #-
  if len(sys.argv) > 1 and sys.argv[1] == "consumer": #- run only consumer (AWS peer2)
    filter_ip = sys.argv[2] if len(sys.argv) > 2 else "52.91.72.141" #-
    consumer(filter_ip) #-
  else: #- local demo with all 3 stages
    c = multiprocessing.Process(target=consumer) #-
    f = multiprocessing.Process(target=filtro) #-
    s = multiprocessing.Process(target=producer) #-
    c.start() #-
    f.start() #-
    s.start() #-
    time.sleep(30) #-
    s.terminate(); f.terminate(); c.terminate() #-
    s.join(); f.join(); c.join() #-

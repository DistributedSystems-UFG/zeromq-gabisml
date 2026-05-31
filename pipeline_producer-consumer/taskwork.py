import zmq, time, pickle, datetime
from constPipe import *  #-

context = zmq.Context()

r = context.socket(zmq.PULL)
r.connect("tcp://" + IP_PRODUCER + ":" + PORT1)   # connect to task source

p = context.socket(zmq.PUSH)
p.bind("tcp://*:" + PORT2)                        

print(f"[FILTER] Stage 2: receiving from {IP_PRODUCER}:{PORT1}, forwarding on port {PORT2}")

while True:
  task = pickle.loads(r.recv())                     

  if task["valor"] < 10:                           
    print(f"[FILTER] Discarding task #{task['id']:04d} (valor={task['valor']} too low)")
    continue

  if task["prioridade"] == "ALTA":                 
    task["valor"] *= 2
    task["boost"] = True
  else:
    task["boost"] = False

  task["processado_por"]   = "filter@peer1"         
  task["timestamp_filter"] = datetime.datetime.now().isoformat()

  print(f"[FILTER] Forwarding task #{task['id']:04d} | valor={task['valor']} | boost={task['boost']}")
  p.send(pickle.dumps(task))                        
import zmq, time, pickle, random
from constPipe import *  #-

def producer():
  context = zmq.Context()
  socket  = context.socket(zmq.PUSH)          # create a push socket
  socket.bind("tcp://*:" + PORT1)              # bind to port (filter connects here)

  print(f"[PRODUCER] Stage 1: sending tasks to Filter on port {PORT1}")
  time.sleep(1)                                # wait for filter to connect

  task_id = 0
  while True:
    task_id += 1
    task = {                                   # new: richer task with priority
      "id":         task_id,
      "valor":      random.randint(1, 100),
      "prioridade": random.choice(["ALTA", "MEDIA", "BAIXA"]),
    }
    print(f"[PRODUCER] Sending task #{task['id']:04d} | valor={task['valor']} | prioridade={task['prioridade']}")
    socket.send(pickle.dumps(task))
    time.sleep(random.uniform(0.3, 1.0))

if __name__ == "__main__":
  producer()

import zmq

context = zmq.Context()
client = context.socket(zmq.PULL)
client.connect('tcp://localhost:6666')

while True:
    msg = client.recv()
    print(msg)
import zmq
import time

context = zmq.Context()
server = context.socket(zmq.PUSH)
server.bind('tcp://*:6666')
count = 0
while True:
    server.send_string('%d' % count)
    print('send', 'count')
    count += 1
    time.sleep(0.2)
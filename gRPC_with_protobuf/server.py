import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse
import threading
import grpc
from concurrent import futures
import paho.mqtt.client as mqtt
import fib_pb2
import fib_pb2_grpc

history=[]

class FibCalculatorServicer(fib_pb2_grpc.FibCalculatorServicer):

    def __init__(self):
        pass

    def Compute(self, request, context):
        n = request.order
        value = self._fibonacci(n)

        response = fib_pb2.FibResponse()
        response.value = value

        return response

    def _fibonacci(self, n):
        a = 0
        b = 1
        if n < 0:
            return 0
        elif n == 0:
            return 0
        elif n == 1:
            return b
        else:
            for i in range(1, n):
                c = a + b
                a = b
                b = c
            return b

class FibHistoryServicer(fib_pb2_grpc.FibHistoryServicer):
    def Compute(self, request, context):
        response = fib_pb2.FibHistoryContext()
        response.history = str(history)
        return response

def on_message(client, obj, msg):
    print(f"TOPIC:{msg.topic}, VALUE:{msg.payload}")
    if msg.topic == "N":
        history.append(int(str(msg.payload)[2:-1]))
        print(history)
    elif msg.topic == "C":
        print(f"TOPIC:{msg.topic}, VALUE:{msg.payload}")
        history.clear()   

def main():
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host="localhost", port=1883)
    client.subscribe('C', 0)
    client.subscribe('N', 0)
    try:
        client.loop_forever()
    except KeyboardInterrupt as e:
        pass

t = threading.Thread(target = main)
t.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8080, type=int)
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer1 = FibCalculatorServicer()
    fib_pb2_grpc.add_FibCalculatorServicer_to_server(servicer1, server)
    servicer2 = FibHistoryServicer()
    fib_pb2_grpc.add_FibHistoryServicer_to_server(servicer2,server)
    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        print(f"Run gRPC Server at {args['ip']}:{args['port']}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass

import grpc

from .device import device_pb2_grpc
from .device.device_pb2 import DeviceId
from .device.device_pb2_grpc import RouteGuideStub


def init_grpc():
    channel = grpc.insecure_channel('127.0.0.1:9001')
    stub = RouteGuideStub(channel)
    return channel, stub

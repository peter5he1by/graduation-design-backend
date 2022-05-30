from abc import ABC, ABCMeta


class DeviceStatus(metaclass=ABCMeta):
    UNKNOWN = 0b0000
    RUNNING = 0b0001
    STOPPED = 0b0010
    MALFUNC = 0b0100
    OFFLINE = 0b1000


if __name__ == '__main__':
    DeviceStatus()

from serial.tools import list_ports


def get_ports():
    return [port for port in list_ports.comports() if port.vid is not None and port.pid is not None]
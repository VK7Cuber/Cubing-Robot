import serial
import struct
import serial.tools.list_ports


def send_massage(array):
    encoding = {"U": 0, "D": 1, "L": 2, "F": 3, "R": 4, "B": 5,
                "U'": 6, "D'": 7, "L'": 8, "F'": 9, "R'": 10, "B'": 11,
                "U2": 12, "D2": 13, "L2": 14, "F2": 15, "R2": 16, "B2": 17}
    connected = False

    arduino = serial.Serial(find_arduino(), 9600)

    while not connected:
        serin = arduino.read()
        connected = True
    for i in array:
        num = encoding[i]
        arduino.write(struct.pack(">B", num))
        is_got = False
        while not is_got:
            ans = arduino.readline().strip()
            print(ans.decode())
            is_got = True
    arduino.close()

def find_arduino():
    ports = serial.tools.list_ports.comports()

    arduino_port = None
    for port in ports:
        if 'USB-SERIAL' in port.description:
            arduino_port = port.device
            break
    return arduino_port
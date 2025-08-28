import serial
import struct
from typing import Iterable, Optional

from config import Config


class ArduinoService:
	ENCODING = {
		"U": 0, "D": 1, "L": 2, "F": 3, "R": 4, "B": 5,
		"U'": 6, "D'": 7, "L'": 8, "F'": 9, "R'": 10, "B'": 11,
		"U2": 12, "D2": 13, "L2": 14, "F2": 15, "R2": 16, "B2": 17
	}

	def __init__(self, port: Optional[str] = None, baudrate: Optional[int] = None):
		self.port = port or Config.ARDUINO_PORT
		self.baudrate = baudrate or Config.ARDUINO_BAUDRATE
		self._arduino: Optional[serial.Serial] = None

	def connect(self) -> None:
		if self._arduino is None:
			self._arduino = serial.Serial(self.port, self.baudrate, timeout=2)
			# Simple handshake (compatible with desktop behavior)
			self._arduino.read(size=1)

	def disconnect(self) -> None:
		if self._arduino is not None:
			self._arduino.close()
			self._arduino = None

	def check_connection(self) -> bool:
		return self._arduino is not None

	def set_motors_speed(self, speed: int) -> None:
		if self._arduino is None:
			raise ConnectionError('Arduino is not connected')
		self._arduino.write(struct.pack(">B", speed))
		self._arduino.readline()

	def send_algorithm(self, moves: Iterable[str]) -> None:
		if self._arduino is None:
			raise ConnectionError('Arduino is not connected')
		for turn in moves:
			number = self.ENCODING[turn]
			self._arduino.write(struct.pack(">B", number))
			self._arduino.readline()

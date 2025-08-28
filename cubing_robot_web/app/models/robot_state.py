import json
import os
from threading import Lock

from config import Config


class RobotState:
	def __init__(self):
		self._lock = Lock()
		self.is_busy = False
		self.current_task = None
		self.connection_status = False
		self._state_path = os.path.join(Config.DATA_DIR, 'robot_state.json')
		self._ensure_data_dir()
		self._load()

	def _ensure_data_dir(self):
		os.makedirs(Config.DATA_DIR, exist_ok=True)

	def _load(self):
		if os.path.exists(self._state_path):
			try:
				with open(self._state_path, 'r', encoding='utf-8') as f:
					data = json.load(f)
				self.is_busy = data.get('is_busy', False)
				self.current_task = data.get('current_task', None)
				self.connection_status = data.get('connection_status', False)
			except Exception:
				pass

	def _save(self):
		data = {
			'is_busy': self.is_busy,
			'current_task': self.current_task,
			'connection_status': self.connection_status,
		}
		with open(self._state_path, 'w', encoding='utf-8') as f:
			json.dump(data, f, ensure_ascii=False, indent=2)

	def lock_robot(self, task_name: str) -> bool:
		with self._lock:
			if self.is_busy:
				return False
			self.is_busy = True
			self.current_task = task_name
			self._save()
			return True

	def unlock_robot(self) -> None:
		with self._lock:
			self.is_busy = False
			self.current_task = None
			self._save()

	def is_robot_available(self) -> bool:
		with self._lock:
			return not self.is_busy

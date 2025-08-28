from functools import wraps
from flask import flash, redirect, url_for

from app.models.robot_state import RobotState


_robot_state = RobotState()


def robot_required(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if not _robot_state.is_robot_available():
			flash('Робот сейчас занят. Подождите завершения текущей задачи.', 'error')
			return redirect(url_for('main.index'))
		return func(*args, **kwargs)
	return wrapper

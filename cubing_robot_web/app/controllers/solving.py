from flask import Blueprint, render_template, request, redirect, url_for, flash

solving_bp = Blueprint('solving', __name__, url_prefix='/solving')


@solving_bp.route('/')
def solving_page():
	return render_template('pages/solving.html')


@solving_bp.route('/solve', methods=['POST'])
def solve_cube():
	# Placeholder: accept cube string and speed from form
	cube = request.form.get('cube')
	speed = request.form.get('speed', type=int)
	if not cube:
		flash('Введите конфигурацию кубика', 'error')
		return redirect(url_for('solving.solving_page'))
	# TODO: integrate rubik-solver and Arduino service
	flash('Алгоритм отправлен роботу (заглушка)', 'success')
	return redirect(url_for('solving.solving_page'))

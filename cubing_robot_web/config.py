class Config:
    SECRET_KEY = 'cubing-robot-secret-key'
    BABEL_DEFAULT_LOCALE = 'ru'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    # Arduino defaults (override via env or instance config if needed)
    ARDUINO_PORT = '/dev/ttyUSB0'  # On Windows during dev you may use 'COM3'
    ARDUINO_BAUDRATE = 9600

    # UI
    THEME_DEFAULT = 'light'

    # Paths
    DATA_DIR = 'cubing_robot_web/data'

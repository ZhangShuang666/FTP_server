import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BIND_HOST = '127.0.0.1'
BIND_PORT = 9992

USER_HOME = os.path.join(BASE_DIR, 'home')

USER_ACCOUNT = {
    'alex': {
        'password': 'alex123',
    },
    'rain': {
        'password': 'rain123'
    }
}


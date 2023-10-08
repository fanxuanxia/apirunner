import os


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
API_TIMEOUT = 5000

FILE_PATH = {
    'config_ini': os.path.join(ROOT_DIR, 'config', 'config.ini'),
    'data': os.path.join(ROOT_DIR, 'data'),
    'logs': os.path.join(ROOT_DIR, 'logs')
}

if __name__ == '__main__':
    print(ROOT_DIR)
    print(FILE_PATH.get('config_ini'))
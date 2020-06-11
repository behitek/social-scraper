import os

PRODUCTION = False
HTTP_PROXY = 'http://10.60.28.99:81'

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def get_data_dir():
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    return DATA_DIR

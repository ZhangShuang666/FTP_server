import sys
from config import settings
from src import service


sys.path.append(settings.BASE_DIR)


if __name__ == '__main__':
    service.MultiServer()

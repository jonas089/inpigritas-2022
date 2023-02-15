from api import main
from client import sync
import threading

if __name__ == '__main__':
    t = threading.Thread(target=sync).start()
    main()

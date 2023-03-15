from api import main
from client import sync
from multiprocessing import Process
from genesis import reset
if __name__ == '__main__':
    reset()
    sync_process = Process(target=sync)
    sync_process.start()
    main()
    sync_process.join()

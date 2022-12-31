from api import main
from node import sync
from multiprocessing import Process, Value
if __name__ == '__main__':
    sync_process = Process(target=sync)
    sync_process.start()
    main()
    sync_process.join()

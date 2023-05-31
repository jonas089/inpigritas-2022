from api import main
from client import sync
from multiprocessing import Process
from genesis import reset

'''
    * main entry point for docker image
    * starts both http server and main synchronisation loop
    * http server consumes events (transfers)
'''
if __name__ == '__main__':
    reset()
    sync_process = Process(target=sync)
    sync_process.start()
    main()
    sync_process.join()

from multiprocessing import Process, Queue
import time

def reader(queue):
    while True:
        msg = queue.get()         
        print msg

def writer(queue):
    x = 0
    while True:   
        queue.put(x)
        x = x + 1
        time.sleep(1)

if __name__=='__main__':
    queue = Queue()
    reader_p = Process(target=reader, args=((queue),))
    reader_p.daemon = True
    reader_p.start()        
    writer(queue)   
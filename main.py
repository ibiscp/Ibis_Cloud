import watch
import threading
import database
import time

class myThread(threading.Thread):
    def __init__(self, threadID, origem, destino, lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.origem = origem
        self.destino = destino
        self.stop = False
        self.lock = lock

    def run(self):
        #print("Starting " + self.name)
        #while (self.stop ==False):
        watch.WatchFolder(self)
        #watch.void(self)
        #print("Exiting " + self.name)

def SaveMap(origem, destino):
    data = [origem, destino]
    database.AddMap(data)


def StartCheck():
    data = database.GetMap()
    threadList = list()

    for tuple in data:
        #print(tuple)
        threadList.append(str(tuple[0]))

    #print(threadList)
    threads = []
    index = 0
    lock = threading.Lock()

    # Create new threads
    for tName in threadList:
        tuple = data[index]
        thread = myThread(tuple[0], tuple[1], tuple[2], lock)
        thread.start()
        threads.append(thread)
        index += 1

    return threads

def aqui():
    # origem = 'C:\\Users\\Ibis\\Desktop\\watch\\Origem2\\'
    # destino = 'C:\\Users\\Ibis\\Desktop\\watch\\Destino2\\'
    # SaveMap(origem, destino)
    threads = StartCheck()

    # time.sleep(30)
    #
    # t = threads[1]
    #
    # print(t)
    #
    # t.stop = True

aqui()
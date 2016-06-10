import os
import win32file
import win32con
import time
#import sync
import threading
#import database

rsync = 0
sleep = 0

def WatchFolder(self):
    global rsync
    global sleep

    ACTIONS = {
      1 : "Created",
      2 : "Deleted",
      3 : "Updated",
      4 : "Renamed from",
      5 : "Renamed to"
    }

    origem = '/cygdrive/D/Users/Desktop/'
    #Remover a ultima barra abaixo para a time machine
    destino = '/cygdrive/C/Users/Ibis/Desktop/watch/Destino/'
    # origem = self.origem
    # destino = self.destino
    path = origem
    backup = '/cygdrive/C/Users/Ibis/Desktop/watch/Backup/'

    t = threading.Thread(target=sincronizar, args = (origem, destino, backup, self))
    t.daemon = False
    #t.start()

    # Thanks to Claudio Grondi for the correct set of numbers
    FILE_LIST_DIRECTORY = 0x0001

    path_to_watch = "D:/"
    #path_to_watch = "D:/Users/Desktop/"
    ibis = os.path.abspath (path_to_watch)

    print(ibis)
    hDir = win32file.CreateFile (
      ibis,
      FILE_LIST_DIRECTORY,
      win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
      None,
      win32con.OPEN_EXISTING,
      win32con.FILE_FLAG_BACKUP_SEMANTICS,
      None
    )

    lastAction = ''

    while (True):#self.stop == False):
      #
      # ReadDirectoryChangesW takes a previously-created
      # handle to a directory, a buffer size for results,
      # a flag to indicate whether to watch subtrees and
      # a filter of what changes to notify.
      #
      # NB Tim Juchcinski reports that he needed to up
      # the buffer size to be sure of picking up all
      # events when a large number of files were
      # deleted at once.
      #

        results = win32file.ReadDirectoryChangesW (
            hDir, # Directory to be monitored
            2048, # Buffer size for the results
            True, # Watch sub tree
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME | # Delete, Create, Rename FILES
             win32con.FILE_NOTIFY_CHANGE_DIR_NAME | # Delete, Create, Rename FOLDER
             win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES | # Update (atributes) FILES AND FOLDER
             win32con.FILE_NOTIFY_CHANGE_SIZE | # Update, when copy FILES
             win32con.FILE_NOTIFY_CHANGE_LAST_WRITE | # Update, when copied FILES update twice
             win32con.FILE_NOTIFY_CHANGE_SECURITY, # Update (security)
            None,
            None
        )

        while results:
            tuple=results[0]

            if not lastAction == tuple:
                # if (tuple[0] == 4):
                #     renamed = results[1]
                #     print(path, tuple[1], "Renamed to", renamed[1])
                #     results.remove(renamed)
                #
                # else:
                    action = ACTIONS.get(tuple[0], "Unknown")
                    print (path, tuple[1], action)
                    data = ([path + tuple[1], action])
                    # u = threading.Thread(target=database.AddLog, args = (data,))
                    # u.daemon = False
                    # u.start()
                    # print(id)

            lastAction = tuple
            results.remove(tuple)

            sleep = time.time()


        # if (rsync == 0):
        #     rsync = 1
        #     t = threading.Thread(target=sincronizar, args = (origem, destino, backup, self))
        #     t.daemon = False
        #     t.start()
        #     #print('Iniciada Thread')
        #     #print(threading.enumerate())


def sincronizar(origem, destino, backup, self):
    global rsync
    global sleep
    #print('Executando Thread')
    while (sleep + 10 > time.time()):
        time.sleep(1)
    self.lock.acquire()
    rsync = 0
    sync.SyncFolder(origem, destino, backup)
    self.lock.release()
    #print('Finalizada Thread')


WatchFolder("D:/Users/Desktop/")


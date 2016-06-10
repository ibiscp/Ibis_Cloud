# from https://libbits.wordpress.com/2011/04/09/get-total-rsync-progress-using-python/

import subprocess
import re
import sys
import time
import datetime

def SyncFolder(origem, destino, backup):

    origem = convertPathToCygdrive(origem)
    destino = convertPathToCygdrive(destino)
    backup = convertPathToCygdrive(backup)

    # Roda o dry run para ver o que precisa ser modificado
    # print('Dry run:')
    cmd = 'rsync -avz --chmod=ugo=rwX --stats --dry-run --delete-excluded ' + origem + ' ' + destino

    proc = subprocess.Popen(cmd,
      shell=True,
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      )

    remainder = str(proc.communicate()[0])
    #ibis = remainder.replace('\\n', '\n')
    #print(remainder)
    #print(ibis)

    #addFolder = list()
    deleteFolder = list()
    addFile = list()
    deleteFile = list()

    try:
        m = re.search(r'file list\\(.*?)\\n\\nNumber of files:', remainder).group(1)
    except:
        m = ''

    #print(m)

    files = m.split('\\n')

    #print(files)

    for f in files:
        if f.startswith('deleting '):
            if f.endswith('/'):
                deleteFolder.append(str(f[9:]))
            else:
                deleteFile.append(str(f[9:]))
        else:
            if not (f.endswith('/') | (f is '')):
                addFile.append(str(f))

    #print('delete folder\n' + str(deleteFolder))
    #print('delete file\n' + str(deleteFile))
    #print('add file\n' + str(addFile))

    ## Total de arquivos baseado na resposta dada pelo Rsync
    #total_files = int(re.findall(r'Number of files transferred: (\d+)', remainder)[0])
    total_files = len(deleteFolder) + len(deleteFile) + len(addFile) #+ len(addFolder)
    total_size = int(re.findall(r'Total transferred file size: (\d+)', remainder)[0])

    print('\nNumber of operations: ' + str(total_files) + ', ' + str(total_size) + ' bytes  ' + convertCygdriveToPath(destino) + '\n')

    if total_files != 0:

        # print('\nReal rsync:')

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')

        ## Comando para fazer backup incremental salvando os modificados na pasta Backup
        cmd = 'rsync -avz --chmod=ugo=rwX  --progress --delete --delete-excluded --backup --backup-dir=' + backup + ' --suffix="' + timestamp + '" ' + origem + ' ' + destino


        proc = subprocess.Popen(cmd,
          #shell=True,
          stdin=subprocess.PIPE,
          stdout=subprocess.PIPE,
        )

        size_transferred = 0
        files_transferred = 0
        noSize = 0

        if total_size == 0:
            total_size = total_files
            noSize = 1

        while True:
            output = str(proc.stdout.readline())
            #print ('\n' + output + '\n')

            if "b''" in output:
                print('')
                break

            elif 'error' in output:
                break

            elif 'deleting' in output:
                files_transferred += 1
                printProgress(files_transferred, total_files, noSize, size_transferred, total_size)

            elif 'to-check' in output:

                files_transferred += 1
                size_transferred = size_transferred + int(re.findall(r'(\d+) 100%', output)[0])
                printProgress(files_transferred, total_files, noSize, size_transferred, total_size)

def printProgress(files_transferred, total_files, noSize, size_transferred, total_size):

    try:
        if noSize:
            sys.stdout.write('\r' + str(files_transferred) + '/' + str(total_files) + ', ' +
                             str('%.2f' %(100 * files_transferred / total_files)) + ' %\n')

        else:
            sys.stdout.write('\r' + str(files_transferred) + '/' + str(total_files) + ', ' +
                             str(size_transferred) + '/' + str(total_size) + ', ' +
                             str('%.2f' %(100 * size_transferred / total_size)) + ' %\n')
    except:
        sys.stdout.write('error\n')

    sys.stdout.flush()

def convertPathToCygdrive(path):

    path = path.replace(":", "")
    path = path.replace("\\", '/')
    path = '/cygdrive/' + path

    return path

def convertCygdriveToPath(cygdrive):

    cygdrive = cygdrive.replace("/cygdrive/", "")
    cygdrive = cygdrive.replace("\\", "/")
    cygdrive = cygdrive[0] + ':' + cygdrive[1:]

    return cygdrive

origem = 'D:\\User\Desktop\Teste'
destino = 'E:\\Data'
backup = 'E:\\Backup'

#SyncFolder(origem, destino, backup)

origem = convertPathToCygdrive(origem)
destino = convertPathToCygdrive(destino)
backup = convertPathToCygdrive(backup)

timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
cmd = 'rsync -a -v -z --chmod=ugo=rwX --exclude=/$RECYCLE.BIN --exclude=/Config.Msi --exclude=/System --progress --delete --delete-excluded --backup --backup-dir=' + backup + ' --suffix="' + timestamp + '" ' + origem + ' ' + destino

print(cmd)
#
# proc = subprocess.call(cmd,
#   shell=True,
#   stdin=subprocess.PIPE,
#   stdout=subprocess.PIPE,
# )

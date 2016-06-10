import mysql.connector
from mysql.connector import errorcode
import time
import datetime

DB_NAME = 'Backup'

def CreateTablesVariable():
    TABLES = {}

    TABLES['Log'] = (
        "CREATE TABLE `Log` ("
        "  `Id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `Path` varchar(200) NOT NULL,"
        "  `Message` varchar(200) NOT NULL,"
        "  `Timestamp` timestamp NOT NULL,"
        "  PRIMARY KEY (`Id`)"
        ") ENGINE=InnoDB")

    TABLES['Map'] = (
        "CREATE TABLE `Map` ("
        "  `Id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `Source` varchar(200) NOT NULL,"
        "  `Destination` varchar(200) NOT NULL,"
        "  PRIMARY KEY (`Id`)"
        ") ENGINE=InnoDB")

    return TABLES

def Connect():

    try:
        cnx = mysql.connector.connect(user='root', password='1123',
                                      host='localhost',
                                      database='ibiscloud')

        #cursor = cnx.cursor()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exists")
        else:
            print(err)

    return cnx

def AddLog(data):

    cnx = Connect()
    cursor = cnx.cursor()

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    add_log = ("INSERT INTO Log "
                   "(Path, Message, Timestamp) "
                   "VALUES (%s, %s, %s)")

    data.append(timestamp)

    # Insert new log
    #cursor.executemany(add_log, data)
    cursor.execute(add_log, data)
    #id = cursor.lastrowid

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

    #return id

def GetMap():

    cnx = Connect()
    cursor = cnx.cursor()

    query = ("SELECT Id, Source, Destination FROM Map ")

    cursor.execute(query)

    data = list()

    for (Id, Source, Destination) in cursor:
      data.append((Id, Source, Destination))

    cursor.close()
    cnx.close()

    return data

def AddMap(data):

    cnx = Connect()
    cursor = cnx.cursor()

    add_map = ("INSERT INTO Map "
                   "(Source, Destination) "
                   "VALUES (%s, %s)")

    # Insert new map
    cursor.execute(add_map, data)
    id = cursor.lastrowid

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

    return id

def UpdateMap(data):

    cnx = Connect()
    cursor = cnx.cursor()

    update_map = ("UPDATE Map SET "
                   "Source=%s, Destination=%s "
                    "WHERE Id=%s")

    # Insert new map
    cursor.execute(update_map, data)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

def DeleteMap(id):

    cnx = Connect()
    cursor = cnx.cursor()

    remove_entry = ("DELETE FROM Map "
                   "WHERE Id LIKE %s")

    cursor.execute(remove_entry, (str(id),))

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

def AddIp(ip):

    cnx = Connect()
    cursor = cnx.cursor()

    add_ip = ("INSERT INTO Ip "
                   "(Address) "
                   "VALUES (%s)")

    # Insert new ip
    cursor.execute(add_ip, [ip])
    id = cursor.lastrowid

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

    return id

def UpdateServerData(data):

    cnx = Connect()
    cursor = cnx.cursor()

    update_ip = ("UPDATE server SET "
                   "Address=%s"
                    "WHERE Id=%s")

    # Insert new map
    cursor.execute(update_ip, data)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

def GetServerData():
    cnx = Connect()
    cursor = cnx.cursor()

    query = ("SELECT Id, Address, User FROM server ")

    cursor.execute(query)

    data = list()

    for (Id, Address, User) in cursor:
        data.append(Address)
        data.append(User)

    cursor.close()
    cnx.close()

    return data

# source = "C:\\Users\\Ibis\\Desktop\\watch\\Origem\\"
# destination="C:\\Users\\Ibis\\Desktop\\watch\\Destino\\"
#
# data = [source, destination]
#
# AddMap(data)

# def CreateDB():
#
#     cursor = Connect().cursor()
#
#     try:
#         cursor.execute(
#             "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
#     except mysql.connector.Error as err:
#         print "Failed creating database: {}".format(err)
#         exit(1)

# def CreateTables():
#
#     TABLES = CreateTablesVariable()
#
#     cnx = Connect()
#     cursor = cnx.cursor()
#
#     for name, ddl in TABLES.items():
#         try:
#             print "Creating table {}: ".format(name), end=''
#             cursor.execute(ddl)
#         except mysql.connector.Error as err:
#             if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#                 print("already exists.")
#             else:
#                 print(err.msg)
#         else:
#             print("OK")
#
#     cursor.close()
#     cnx.close()

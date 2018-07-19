import mysql.connector
import struct
from time import sleep
import ctypes


def main():

    MAXROWS = 1000; #maximum number of rows to transfer per connection / commit

    #set window title
    ctypes.windll.kernel32.SetConsoleTitleA("2syncToCloud.py")
    
    #loop process of reading and inserting into SQL table
    while True:

        #establish SQL cnxn to two73.com
        try:
            SQLCloudCnxn = mysql.connector.connect(user='STLprototype', password='Npe5f356nWkC11z59753DP03D715O8UM',
                                              host='23.229.161.9',
                                              database='STL_Prototype')
            SQLCloudCursor = SQLCloudCnxn.cursor()
        except Error as error:
            print(error)

        #establish local SQL cnxn
        try:
            SQLLocalCnxn = mysql.connector.connect(user='root', password='',
                                              host='localhost',
                                              database='prototype')
            SQLLocalCursor = SQLLocalCnxn.cursor()
        except LocalError as error:
            print(error)
        
        query = "SELECT `key` FROM logdata ORDER BY `key` DESC LIMIT 1"
        
        SQLCloudCursor.execute(query)
        remoteKey = SQLCloudCursor.fetchone()[0]
        
        SQLLocalCursor.execute(query)
        localKey = SQLLocalCursor.fetchone()[0]

        keyDiff = localKey - remoteKey
        if (keyDiff > MAXROWS):
            keyDiff = MAXROWS;
            localKey = remoteKey + MAXROWS

        print("syncing rows %s through %s..." % (remoteKey, localKey))
        
        query = "SELECT * FROM logdata WHERE `key` > %s AND `key` <= %s ORDER BY `key` DESC LIMIT %s"
        SQLLocalCursor.execute(query, (remoteKey, localKey, keyDiff,))
        newRows = SQLLocalCursor.fetchall()
        print("got %s new rows" % keyDiff)

        for row in reversed(newRows):
            query = "INSERT INTO logdata " \
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, " \
                           "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, " \
                           "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, " \
                           "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, " \
                           "%s,%s,%s,%s,%s,%s)"
            SQLCloudCursor.execute(query, row)
            print(row[0], "remote row inserted")

        SQLCloudCnxn.commit()
        
        sleep(2)

if __name__ == '__main__':
    main()

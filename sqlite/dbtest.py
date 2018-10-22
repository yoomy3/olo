#-*-coding:utf-8-*-

import sys

import os.path
import time
import sqlite3

############################################################

lastUpdatedTime = 0;

basepath = os.path.abspath(os.path.dirname(__file__))
# filepath = os.path.join(basepath, "list.txt")
filepath = os.path.join(basepath, "exported_tracks.txt")
dbpath = os.path.join(basepath, "..\\test.db")
lines = [line.rstrip('\n') for line in open(filepath, encoding='utf-8')]

# print(filepath);
# print(lines);


## SELECT * FROM musics LIMIT 1 OFFSET 5132;


############################################################

def createTable(cur):
    # Create table
    # create year, month, daytime columns
    cur.execute('''CREATE TABLE IF NOT EXISTS musics (
                 time integer primary key,
                 song text not null,
                 artist text not null,
                 album text not null,
                 year integer not null,
                 month integer not null,
                 timeofday integer not null)''')

def insertTracks(cur):
    for line in lines:
        l = line.split('\t')
        l[0] = int(l[0])
        # TODO: calculate the date for each song
    #    print(time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(l[0])));
        trackTime = time.localtime(l[0])
        trackTime_year = trackTime[0]
        trackTime_month = trackTime[1]
        # use total minutes as time in a day (= hour*60 + min)
        trackTime_day = trackTime[3]*60+trackTime[4]
        l.extend([trackTime_year, trackTime_month, trackTime_day]);
    #    print(l);
        cur.execute("INSERT OR IGNORE INTO musics VALUES(?,?,?,?,?,?,?)", l);
        # TODO: Cross-check with spotify if the song really exists


def clearTable(cur, tableName):
    cur.execute("DELETE FROM ?", tableName)
    cur.execute("VACUUM")

def dropTable(cur, tableName):
    cur.execute("DROP TABLE ?", tableName)

def createIndex(cur, indexName, tableName, colName):
    cur.execute("CREATE INDEX ? ON ? (?)", indexName, tableName, colName)

def dropIndex(cur, indexName):
    cur.execute("DROP INDEX ?", indexName)

def select_all(cur):
    i = 0
    cur.execute("SELECT * FROM musics")
    rows = cur.fetchall()
    for row in rows:
        i += 1
    print(i)

def select_year(cur):
    i = 0
    cur.execute("SELECT * FROM musics ORDER BY year ASC")
    rows = cur.fetchall()
    for row in rows:
        i += 1
    print(i)

############################################################

conn = sqlite3.connect(dbpath);
cur = conn.cursor()

# createIndex(cur, '_year', 'musics', 'year')
# createIndex(cur, '_month', 'musics', 'month')
# createIndex(cur, '_day', 'musics', 'timeofday')

# dropIndex(cur, '_year')
# dropIndex(cur, '_month')
# dropIndex(cur, '_day')

select_year(cur)

# clearTable(cur, 'musics');
#
# # TODO: create index on year, month and daytime
#
# # TODO: test the performance
#
# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

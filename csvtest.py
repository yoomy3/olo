# Script to divide massive Last.fm listening history into a 'life', 'year' and 'day' timeframe
# --------------------------------------------------------------------------------------------

# Tickets
# > Need to account for timezones in daytimestamp
# > open up new branch to incorporate resolution
# > Did this come through?

import csv
import datetime
import calendar
import time
import sh
sh.init()
from oloFunctions import *
resolution = int(raw_input('resolution? '))

filename = 'tracks/exported_tracks.txt'
lifename = str.split(filename, '.txt')[0] + '_life.txt'
yearname = str.split(filename, '.txt')[0] + '_year.txt'
dayname = str.split(filename, '.txt')[0] + '_day.txt'

class col:
    prp = '\033[95m'
    vio = '\033[94m'
    gre = '\033[92m'
    yel = '\033[93m'
    ora = '\033[91m'
    none = '\033[0m'
    red = '\033[1m'
    und = '\033[4m'

yesorno = col.none + '[ ' + col.gre + 'Y' + col.none + ' / ' + col.red + 'N' + col.none + " ] "

then = time.time()
lifetime = 0
yeartime = 0
daytime = 0

togglesort = raw_input(col.yel + 'sort? ' + yesorno )
if togglesort == 'Y' or togglesort == 'y':
    togglesort = True
else:
    togglesort = False

if togglesort:
    toggleprint = raw_input(col.yel + 'print all output? ' + col.none + '[ ' + col.gre + 'Y' + col.none + ' / ' + col.red + 'N' + col.none + " ] "  )
    if toggleprint == 'Y' or toggleprint == 'y':
        toggleprint = True
    else:
        toggleprint = False


    with open(filename,'rb') as f:
        reader = csv.reader(f, delimiter = '\t' )
        print 'ok, now sorting...'

        # sort by life
        # =====================================================
        f.seek(0)
        with open(lifename, 'w') as wl:
            writer = csv.writer(wl, delimiter = '\t')
            data = sorted(f, key = lambda row: str.split(row, '\t')[0])
            print 'sorted!'
            sortedreader = csv.reader(data, delimiter='\t')
            for row in sortedreader:
                if toggleprint:
                    #print data
                    print row[0]
                    print 'datetime: ' + str(convertTimestamp(row[0]))
                    print row[1] + '  -  ' + row[2]
                    print col.gre + '- - - - - - - - - - - - - - -' + col.none
                writer.writerow(row)
        lifetime = time.time() - then

        # sort by year
        # =====================================================
        now = time.time()
        with open(lifename, 'r') as life:
            lifereader = csv.reader(life, delimiter = '\t' )
            f.seek(0)
            with open(yearname, 'w') as wl:
                writer = csv.writer(wl, delimiter = '\t')
                data = sorted(life, key = lambda row: yearTimestamp(str.split(row, '\t')[0]))
                print 'sorted!'
                sortedreader = csv.reader(data, delimiter='\t')
                for row in sortedreader:
                    if toggleprint:
                        #print data
                        print row[0]
                        print 'datetime: ' + str(convertTimestamp(row[0]))
                        print row[1] + '  -  ' + row[2]
                        print col.prp + '- - - - - - - - - - - - - - -' + col.none
                    writer.writerow(row)
            yeartime = time.time() - now


        # sort by day
        # =====================================================
        now = time.time()
        f.seek(0)
        with open(dayname, 'w') as wl:
            writer = csv.writer(wl, delimiter = '\t')
            data = sorted(f, key = lambda row: dayTimestamp(str.split(row, '\t')[0])[0])
            print 'sorted!'
            sortedreader = csv.reader(data, delimiter='\t')
            for row in sortedreader:
                if toggleprint:
                    #print data
                    print 'datetime: ' + str(convertTimestamp(row[0]))
                    print row[1] + '  -  ' + row[2]
                    print col.red + '- - - - - - - - - - - - - - -' + col.none
                writer.writerow(row)
        daytime = time.time() - now
    print 'total sorting time: ' + str(time.time() - then)
    print 'life: ' + str(lifetime)
    print 'year: ' + str(yeartime)
    print 'day: ' + str(daytime)

#       _           _           _            _
#   /\ ) \      /\ ) \      /\ ) \      /\ ) \
# <=()=>  )   <=()=>  )   <=()=>  )   <=()=>  )
#   || )_/      || )_/      || )_/      || )_/
#   ||          ||          ||          ||
#   ||          ||          ||          ||
# Chop up the sorted lists into sublists
# =====================================================
# LIFE TIMEFRAME
print col.und + 'LIFE SUBLISTS' + col.none
path = 'tracks/life/'
with open(lifename, 'r') as rl:
    reader = csv.reader(rl, delimiter ='\t')
    first = int(reader.next()[0])
    print 'first: ', first
    for row in reader:
        last = row
    last = int(last[0])
    print 'last: ' + str(last)
    segduration = (last - first) / resolution
    print 'segduration ', segduration
    rl.seek(0)
    for sublist in range(resolution):
        sublistname = 'sl_life_' + str(sublist) + '.txt'
        with open(path + sublistname, 'w') as wl:
            writer = csv.writer(wl, delimiter = '\t')
            for row in reader:
                if (int(row[0])-first) < segduration * (sublist + 1):
                    # print row
                    row.append(convertTimestamp(row[0]))
                    writer.writerow(row)
                else:
                    break

# YEAR TIMEFRAME
print col.und + 'YEAR SUBLISTS' + col.none
path = 'tracks/year/'
segduration = (3600 * 24 * 365) / resolution
with open(yearname, 'r') as rl:
    reader = csv.reader(rl, delimiter ='\t')
    for sublist in range(resolution):
        sublistname = 'sl_year_' + str(sublist) + '.txt'
        with open(path + sublistname, 'w') as wl:
            writer = csv.writer(wl, delimiter = '\t')
            for row in reader:
                if yearTimestamp(row[0])[1] < segduration * (sublist + 1):
                    row.append(convertTimestamp(row[0]))
                    writer.writerow(row)
                else:
                    #writer.writerow(['!!!'])
                    print('!!!')
                    break


# DAY TIMEFRAME
print col.und + 'DAY SUBLISTS' + col.none
path = 'tracks/day/'
segduration = (3600 * 24) / resolution
with open(dayname, 'r') as rl:
    reader = csv.reader(rl, delimiter ='\t')
    for sublist in range(resolution):
        sublistname = 'sl_day_' + str(sublist) + '.txt'
        with open(path + sublistname, 'w') as wl:
            writer = csv.writer(wl, delimiter = '\t')
            for row in reader:
                if dayTimestamp(row[0])[1] < segduration * (sublist + 1):
                    row.append(convertTimestamp(row[0]))
                    writer.writerow(row)
                else:
                    #writer.writerow(['!!!'])
                    print(str(sublist) + ' !!! '),
                    break

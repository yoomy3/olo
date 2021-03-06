"""
#        _                       _ _
#   ___ | | ___    _ __ __ _  __| (_) ___
#  / _ \| |/ _ \  | '__/ _` |/ _` | |/ _ \
# | (_) | | (_) | | | | (_| | (_| | | (_) |
#  \___/|_|\___/  |_|  \__,_|\__,_|_|\___/
#
# ==============================================================
#      ---   Exploring metadata as a design material   ---
# ==============================================================

Tickets
- try reading values from MCP without other GPIO pins configured

"""
#from oloFunctions import *
#              _____
#  ______________  /____  _________
#  __  ___/  _ \  __/  / / /__  __ \
#  _(__  )/  __/ /_ / /_/ /__  /_/ /
#  /____/ \___/\__/ \__,_/ _  .___/
#  ========================/_/====

import sh
sh.init()
import time
import RPi.GPIO as gpio
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from oloFunctions import *

"""
\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\
Migratable to sh.py or oloFunctions
=\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==
"""
class col:
    prp = '\033[95m'
    vio = '\033[94m'
    gre = '\033[92m'
    yel = '\033[93m'
    ora = '\033[91m'
    none = '\033[0m'
    red = '\033[1m'
    und = '\033[4m'

def exectime(then):
    now = time.time()
    extime = now - then
    return "{0:.6f}".format(round(extime,7))

def timeframe():
    if sh.values[2] < 10:
        if sh.values[3] < 10:
            # (0, 0)
            sh.timeframe = 'life '
            return 0
        else:
            # (0, 1)
            sh.timeframe = 'year '
            return 1
    else:
        if sh.values[3] < 10:
            # (1, 0)
            sh.timeframe = 'day  '
            return 2
        else:
            # (1, 1)
            sh.timeframe = 'err  '
            return -1
    sh.timeframe = 'unkn '
    return -2
"""
\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\
=\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==
"""


print sh.CLK
mcp = Adafruit_MCP3008.MCP3008(clk=sh.CLK, cs=sh.CS, miso=sh.MISO, mosi=sh.MOSI)

# GPIO configuration:
gpio.setup(sh.switch1, gpio.IN) #gpio 16  - three pole switch 1
gpio.setup(sh.switch2, gpio.IN) #gpio 18  - three pole switch 2

print('Reading MCP3008 values, press Ctrl-C to quit...')

#  ______
#  ___  /___________________
#  __  /_  __ \  __ \__  __ \
#  _  / / /_/ / /_/ /_  /_/ /
#  /_/  \____/\____/_  .___/
# ===================/_/===

while(True):
    # Read all the ADC channel values in a list.
    then = time.time()
    readValues()
    #print(col.yel + 'readvals exec time: ' + str(exectime(then)) + col.none)
    # Print the ADC values.
    then = time.time()
    #print sh.values[0]
    timeframe()
    #print col.red + sh.timeframe + col.none
    printValues(sh.values)

    #print('printvals exec time: ' + str(exectime(then)))

    # Pause for half a second.
    #time.sleep(0.5)

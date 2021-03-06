try: # try importing libraries that only run locally on RPi. While testing on desktop, these are not available nor required.
    import Adafruit_MCP3008
    import RPi.GPIO as gpio
except:
    pass
import time
import sh
import datetime

class col:
    prp = '\033[95m'
    vio = '\033[94m'
    gre = '\033[92m'
    yel = '\033[93m'
    ora = '\033[91m'
    none = '\033[0m'
    red = '\033[1m'
    und = '\033[4m'

# Software SPI configuration:
try:
    mcp = Adafruit_MCP3008.MCP3008(clk = sh.CLK, cs = sh.CS, miso = sh.MISO, mosi = sh.MOSI)
    gpio.setup(17, gpio.IN) #gpio 17  - three pole switch 1
    gpio.setup(18, gpio.IN) #gpio 18  - three pole switch 2
except:
    pass

def convertTimestamp(tstamp):
    _dt = datetime.datetime.fromtimestamp(int(tstamp))
    return _dt

def yearTimestamp(tstamp):
    tstamp = int(tstamp)
    year = datetime.datetime.fromtimestamp(tstamp).strftime('%Y')
    _yt = int(time.mktime(time.strptime(year, '%Y')))# epoch time of Jan 1st 00:00 of the year of the song
    _dt = datetime.datetime.fromtimestamp(int(tstamp - _yt))
    return _dt, int(tstamp - _yt)

def dayTimestamp(tstamp):
    tstamp = int(tstamp)
    pattern = '%Y %m %d'
    day = datetime.datetime.fromtimestamp(tstamp).strftime(pattern)
    _dayt = int(time.mktime(time.strptime(day + ' 00 : 00 : 00', pattern + ' %H : %M : %S' ))) # epoch time since beginning of the day
    _dt = datetime.datetime.fromtimestamp(int(tstamp - _dayt + (25200))) # account for time zone
    return _dt, int(tstamp - _dayt + 0) #(25200))


def timeframe():
    # function that updates sh.timeframe
    def checksame():
        if sh.timeframe == sh.prevtimeframe:
            return 1
        else:
            return 0
    sh.prevtimeframe = sh.timeframe
    if sh.values[2] < 10:
        if sh.values[3] < 10:
            # (0, 0)
            sh.timeframe = 'life'
            if sh.timeframe == sh.prevtimeframe:
                return 1
            else:
                return 0
        else:
            # (0, 1)
            sh.timeframe = 'year'
            if sh.timeframe == sh.prevtimeframe:
                return 1
            else:
                return 0
    else:
        if sh.values[3] < 10:
            # (1, 0)
            sh.timeframe = 'day '
            if sh.timeframe == sh.prevtimeframe:
                return 1
            else:
                return 0
        else:
            # (1, 1)
            sh.timeframe = 'err  '
            return -1
    sh.timeframe = 'unkn '
    return -2


def readValues():
    # Read all the ADC channel values in a list.
    sh.values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        sh.values[i] = mcp.read_adc_difference(i)
    return sh.values


def printValues(vals):
    # Function that prints the values from all 8 channels of the ADC to screen
    newVals = [0] * 8
    for i in range(8):
        newVals[i] = vals[i]
    print(newVals[0])
    # Pause for half a second.
    #time.sleep(0.5)


def moveslider(_target):
    # Function that moves the slider to a specified position (0 - 1024)
    prev = 0
    touch = 0
    errormargin = 8 # makes the width of a target 16 which is close to the slowest movement
    slowrange = 150

    if (_target >= 0 and _target <= 1024):
        while (distance(_target) > errormargin):
            #print('motor loop')
            if (sh.values[sh.touch_ch] > 1): # if capacitive touch is touched
                print 'motor touched, waiting...'
                hardstop()
                prev = 0
            else:
                if sh.values[sh.slider_ch] > _target:
                    # If the slider is to the right of the right of the target
                    if distance(_target) > slowrange:
                        # Fast movement
                        print(col.yel + 'tar: ' + col.none + str(_target) + col.yel + '  cur: ' + col.none  + str(sh.values[sh.slider_ch]) + col.prp + ' <<o---' + col.none)
                        gpio.output(sh.mRight, False)
                        gpio.output(sh.mLeft, True)
                    else:
                        # Slow movement
                        print(col.yel + 'tar: ' + col.none + str(_target) + col.yel + '  cur: ' + col.none  + str(sh.values[sh.slider_ch]) + col.vio + ' <<o-  ' + col.none)
                        duty = 0.007
                        gpio.output(sh.mLeft, True)
                        time.sleep(duty)
                        gpio.output(sh.mLeft, False)
                        time.sleep(0.01 - duty)
                if sh.values[sh.slider_ch] < _target:
                    # If the slider is to the right of the left of the target
                    if distance(_target) > slowrange:
                        # Fast movement
                        print(col.yel + 'tar: ' + col.none + str(_target) + col.yel + '  cur: ' + col.none  + str(sh.values[sh.slider_ch]) + col.red + ' ---o>>' + col.none)
                        gpio.output(sh.mLeft, False)
                        gpio.output(sh.mRight, True)
                    else:
                        # Slow movement
                        print(col.yel + 'tar: ' + col.none + str(_target) + col.yel + '  cur: ' + col.none  + str(sh.values[sh.slider_ch]) + col.ora + '   -o>>' + col.none)
                        duty = 0.007
                        gpio.output(sh.mRight, True)
                        time.sleep(duty)
                        gpio.output(sh.mRight, False)
                        time.sleep(0.01 - duty)
            readValues()
        # turn off motor and print location
        hardstop()
        readValues()
        print 'motor move complete: '
        print 'position: ' + str(sh.values[sh.slider_ch])
    else:
        print '[moveSlider] improper value given!'


def hardstop():
    # Function to stop the slider from moving
    for t in range(5):
        gpio.output(sh.mLeft, True)
        gpio.output(sh.mRight, True)
    gpio.output(sh.mLeft, False)
    gpio.output(sh.mRight, False)
    print('hard stop')


def distance(_target):
    # Function to calculate the distance between the current position of the slider knob
    # and an inputted value '_target'
    readValues()
    return abs(sh.values[sh.slider_ch] - _target)

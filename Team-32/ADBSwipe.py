#! python3

import os
from numpy import linspace

locationToPushTo = "/data/local/tmp/"
eventDevice = "/dev/input/event0"

adb = "adb "
shell = "shell "
adbShell = adb + shell

def startTouch():
    return "sendevent {device} 3 57 1337;sendevent {device} 1 330 1;sendevent {device} 1 325 1;".format(device = eventDevice)

def endTouch():
    return "sendevent {device} 3 57 4294967295;sendevent {device} 1 330 0;sendevent {device} 1 325 0;sendevent {device} 0 0 0;".format(device = eventDevice)

def swipe(coords):
    commands = ""
    for coord in coords:
        commands += "sendevent {device} 3 53 {x};sendevent {device} 3 54 {y};sendevent {device} 0 0 0;".format(device = eventDevice, x = coord[0], y = coord[1])
    return commands

def run(command):
    """ adb has a hard limit of 4096 bytes that can be sent through, write to file and push file to get around that """
    if type(command) is Command:
        command = command.str()
    print("running {}".format(command))
    with open("command", "w") as o:
        o.write(command)
    os.popen(adb + "push command " + locationToPushTo)
    return os.popen(adbShell + "sh " + locationToPushTo + "command").read()

def runMultiple(command):
    if type(command) is Command:
        command = command.str()
    # split command into just under max length and send those

def runSimple(command):
    """ Used for running single (or short) commands over adb """
    if type(command) is Command:
        command = command.str()
    print("running {}{}".format(adbShell, command))
    return os.popen(adbShell + command).read()

def line(*coords, num=2):
    """ Given 2 (x, y) coords, returns a list of coords that draws a line between the two including the ends """
    xs = linspace(coords[0][0], coords[1][0], num=num, dtype=int)
    ys = linspace(coords[0][1], coords[1][1], num=num, dtype=int)
    return list(zip(xs, ys))

def getScreenSize():
    """ Note this requires the android device to have wm """
    output = runSimple("wm size")
    output = output[:-1] # Remove the trailing newline
    output = output.split(": ")[1] # extract just the WidthxHeight
    output = output.split("x") # extract the width and height into a list
    return output

def sleep(time=.5):
    return "sleep {};".format(time)

def multiSwipe(listOfSwipes):

    return

class Command:
    commandString = ""

    def add(self, command):
        self.commandString += str(command)
    def str(self):
        return self.commandString
    def reset(self):
        self.commandString = ""

"""
[(x1,y1), (x2, y2), (x3, y3)]

"""

cmd = Command()

# wake device
runSimple("input keyevent 26")

# swipe up
cmd.add(startTouch())
cmd.add(swipe(line((300, 2000), (900, 500), num=10)))
cmd.add(endTouch())

cmd.add(sleep())

# lock code
cmd.add(startTouch())
# bottom row
cmd.add(swipe(line((340, 2100), (1100, 2000))))
# up one
cmd.add(swipe(line((1100, 2000), (1120, 1700))))
# up left
cmd.add(swipe(line((1120, 1700), (700, 1300))))
cmd.add(endTouch())

run(cmd)




"""
Notes:
Best Example: https://github.com/mattwilson1024/android-pattern-unlock/blob/master/unlock.sh
"getevent command captures everything in hexadecimal, but the command sendevent, requires everything to be in decimal" https://qatesttech.wordpress.com/2012/06/21/turning-the-output-from-getevent-into-something-something-that-can-be-used/
http://ktnr74.blogspot.com/2013/06/emulating-touchscreen-interaction-with.html:
For touch events only 2 event types are used:
EV_ABS (3)
EV_SYN (0)
EV_KEY (1)

Touching the display (in case of Type A protocol) will result in an input report (sequence of input events) containing the following event codes:
ABS_MT_TRACKING_ID (57) - ID of the touch (important for multi-touch reports)
ABS_MT_POSITION_X (53) - x coordinate of the touch
ABS_MT_POSITION_Y (54) - y coordinate of the touch
ABS_MT_TOUCH_MAJOR (48) - basically width of your finger tip in pixels
ABS_MT_TOUCH_MINOR (49) - minor axis of the width of the finger?
ABS_MT_PRESSURE (58) - pressure of the touch
SYN_MT_REPORT (2) - end of separate touch data
SYN_REPORT (0) - end of report
BTN_TOUCH (330) - touch down/up
BTN_TOOL_FINGER (325) - finger down/up

Let's say we want to emulate a touch down event at the point with coordinates x=300, y=400. We will need to execute the following sendevent commands:

sendevent /dev/input/event0 3 57 0
sendevent /dev/input/event0 3 53 300
sendevent /dev/input/event0 3 54 400
sendevent /dev/input/event0 3 48 5
sendevent /dev/input/event0 3 58 50
sendevent /dev/input/event0 0 2 0
sendevent /dev/input/event0 0 0 0

The release report is really simple. To let the input device know that all previous touches have been released - you just send the empty report with ABS_MT_TRACKING_ID = -1:

ABS_MT_TRACKING_ID (57)
SYN_MT_REPORT (2)
SYN_REPORT (0)

sendevent /dev/input/event0 3 57 -1
sendevent /dev/input/event0 0 2 0
sendevent /dev/input/event0 0 0 0

sends power button
adb shell input keyevent 26
"""

#! python3

"""
Plan of Attack:
construct the string to send over adb
send the string over adb
"""

import os

eventDevice = "/dev/input/event0"
adb = "adb shell "

def startTouch():
    print("start touch")
    return "sendevent {device} 3 57 1337;".format(device = eventDevice)

def endTouch():
    print("end touch")
    return "sendevent {device} 3 57 4294967295;sendevent {device} 0 0 0;sendevent {device} 0 48 6;sendevent {device} 0 49 6;sendevent {device} 0 0 0;".format(device = eventDevice)

def multiSwipe(swipes):
    print("multiSwipe")
    commands = ""
    for swipe in swipes:
        commands += "sendevent {device} 3 53 {x};sendevent {device} 3 54 {y};sendevent {device} 0 0 0;".format(device = eventDevice, x = swipe[0], y = swipe[1])
    return commands
#sendevent {device} 3 58 50;sendevent {device} 3 48 5;

def run(command):
    print("running {}{}".format(adb, command))
    return os.popen(adb + command).read()

# wake device
run("input keyevent 26")

commands = startTouch()

coords = [(800, 900)]
commands += multiSwipe(coords)

commands += endTouch()


run(commands)




"""
Notes:
Best Example: https://github.com/mattwilson1024/android-pattern-unlock/blob/master/unlock.sh
"getevent command captures everything in hexadecimal, but the command sendevent, requires everything to be in decimal" https://qatesttech.wordpress.com/2012/06/21/turning-the-output-from-getevent-into-something-something-that-can-be-used/
http://ktnr74.blogspot.com/2013/06/emulating-touchscreen-interaction-with.html:
For touch events only 2 event types are used:
EV_ABS (3)
EV_SYN (0)

Touching the display (in case of Type A protocol) will result in an input report (sequence of input events) containing the following event codes:
ABS_MT_TRACKING_ID (57) - ID of the touch (important for multi-touch reports)
ABS_MT_POSITION_X (53) - x coordinate of the touch
ABS_MT_POSITION_Y (54) - y coordinate of the touch
ABS_MT_TOUCH_MAJOR (48) - basically width of your finger tip in pixels
ABS_MT_TOUCH_MINOR (49) - minor axis of the width of the finger?
ABS_MT_PRESSURE (58) - pressure of the touch
SYN_MT_REPORT (2) - end of separate touch data
SYN_REPORT (0) - end of report

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

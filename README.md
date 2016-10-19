https://github.com/fireflyes/Team-32-tsum-

TsumTsum AI

Team-32-tsum- is a program for CST 205 at CSUMB due 10.14.2016

Coded by David Keller, Alex Alkire, and Peter Pommer


Abstract:
	
	It 'plays' the Android game TsumTsum by 'looking' through a webcam to parse the game play area using OpenCV, and sends swipe events via adb and Android's GetEvent.
	It uses circle detection to find the tsums on the screen, then uses histograms to detect and aggregate tsums of the same type, which is then passed to a solving algorithm that returns a list of groups of tsums to be swiped, which is then passed to a function that generates, sends, and runs those swipes to the Android device.

How to run:
	
	Requirements:
	
		adb installed and added to $PATH
		Android phone with 'wm'
		Android phone plugged in via usb cable
		Android phone with usb debugging enabled
		
	Plug in phone to the computer.
	Run the TsumTsum game app on the phone
	Run this program
	Place the phone's screen in front of the computers webcam
	Position the screen so it is in the green box
	Done! Watch the game get played.

Future work:

	Auto discover screen and screen rotation
	Multi touch swipes
	Code optimizations
	Handle large Tsums
	More game modes and handling of 'good' moves with power ups
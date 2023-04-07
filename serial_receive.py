from serial import *
from time import time
from time import sleep

port = Serial('COM15', 115200, timeout=0, bytesize=8, parity='N', stopbits=1)

#denote a controller deadzone so the drone stops moving below this angle (relative to 0)
deadzone = 15 

#read serial line in, timeout in case nothing is received
def readSerialLine(port, timeout):
    start_time = time()
    line = ''
    while True:
        data = port.read().decode('utf-8')
        line += data

        if line.endswith('\r\n') or (time() - start_time) > timeout:
            break
    return line[:-2] #return the line regardless if we got data for not, minus the return characters

#split the serial line and return an array of values from microbit controllers
def splitLine(line):
    return line.strip().split('|')

#check if a value exceeds limit of deadzone
def checkDeadzone(val, angle):
    if abs(val) > angle:
        return True
    return False

while True:
    line = splitLine(readSerialLine(port, 0.5))
    currPitch = 0
    currRoll = 0
    currAlt = 0
    currYaw = 0
    if len(line) >= 4:
        currPitch = int(line[0])
        currRoll = int(line[1])
        currAlt = int(line[2])
        currYaw = int(line[3])

    #if checkDeadzone(currPitch, deadzone):
    print("FB: " + str(currPitch))
    #if checkDeadzone(currRoll, deadzone):
    print("LR: " + str(currRoll))
    print("UD: " + str(currAlt))
    print("Yaw: " + str(currYaw))

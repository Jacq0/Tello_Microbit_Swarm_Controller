from serial import *
from time import time
from time import sleep

#the port of the microbit receiver
microbit = 'COM15'

port = Serial(microbit, 115200, timeout=0, bytesize=8, parity='N', stopbits=1)

#denote a controller deadzone so the drone stops moving below this angle (relative to 0)
deadzone = 0.15

#range of the angles of joystick movement
angleRange = 45

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

#separate the list into control and takeoff/land values
def getControlValues(list):
    if len(list) == 6:
        return list[0:4]

def getTakeoffLandValues(list):
    if len(list) == 6:
        return list[-2:]

#split the serial line and return an array of values from microbit controllers
def splitLine(line):
    return line.strip().split('|')

#check if a value exceeds limit of deadzone
def checkDeadzone(val, angle):
    if abs(val) > angle:
        return True
    return False

#read the serial line, split it and normalise the values before return.
def returnInputValues():
    line = splitLine(readSerialLine(port, 0.5))
    control = calculateReturnValues(listToFloat(getControlValues(line)), deadzone)
    tol = getTakeoffLandValues(line)

    inputs = [control, tol]

    return inputs
    
def listToFloat(list):
    newList = []

    for i in list:
        if i != '':
            newList.append(float(i))

    return newList

def normalise(val, range):
    if val > range:
        val = 45
    if val < -range:
        val = -45
    
    return val/range

#calculate a normalised values list, 0 if inside the deadzone
def calculateReturnValues(values, deadzone):
    returnVals = []

    for val in values:
        nVal = normalise(val, angleRange)

        if nVal < deadzone and nVal > -deadzone:
            returnVals.append(0)
        else:
            returnVals.append(nVal)

    return returnVals
            
def testMethod():
    while True:
        controls = returnInputValues()
        currPitch = 0
        currRoll = 0
        currAlt = 0
        currYaw = 0
        takeoff = 0
        land = 0
        if len(controls) >= 2:
            currPitch = controls[0][0]
            currRoll = controls[0][1]
            currAlt = controls[0][2]
            currYaw = controls[0][3]
            takeoff = controls[1][0]
            land = controls[1][1]

        #if checkDeadzone(currPitch, deadzone):
        print("FB: " + str(currPitch))
        #if checkDeadzone(currRoll, deadzone):
        print("LR: " + str(currRoll))
        print("UD: " + str(currAlt))
        print("Yaw: " + str(currYaw))
        print("Takeoff: " + str(takeoff))
        print("Land: " + str(land))

#run test method if not imported
if __name__ == "__main__":
    testMethod()
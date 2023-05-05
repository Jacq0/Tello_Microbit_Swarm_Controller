from djitellopy import TelloSwarm
import serial_receive as sr
import time

#if the program is running or not
running = True
inFlight = False
batteryChecked = False

#the time interval so we don't spam the drones with commands.
lastTick = int(time.time() * 1000) #time in millis
lastChange = int(time.time() * 1000)
interval = 100

#the IP addresses of the tello drones
ips = ["192.168.1.3","192.168.1.4"]
batteryVal = []
numDrones = len(ips)
counter = 0 #counter that holds a value corresponding to which drone to control

controlsDisabled = False

swarm = TelloSwarm.fromIps(ips)
swarm.connect()

def landDrones():
    for drone in swarm:
        drone.land()

def takeoffDrones():
    global counter
    i = 0
    for drone in swarm:
        drone.takeoff()

def sendControls(fb, ud, lr, yaw, speed):
    global counter
    i = 0
    for drone in swarm:
        if counter == 0 or i == (counter-1):
            drone.send_rc_control(int(lr*speed), int(fb*speed), int(ud*speed), int(yaw*speed))
        else:
            drone.send_rc_control(0,0,0,0)
        i = i + 1

def stopDrones():
    for drone in swarm:
        drone.send_rc_control(0,0,0,0)

def iterateCounter():
    global counter

    #add a 500ms delay so the count doesn;t change rapidly
    if (lastChange+250) < int(time.time() * 1000):
        counter = counter + 1
        if counter >= numDrones+1:
            counter = 0

def disableControls():
    global controlsDisabled
    controlsDisabled = not controlsDisabled

def checkBattery():
    for drone in swarm:
        batteryVal.append(drone.get_battery())
    
while running:
    try:
        values = sr.returnInputValues()

        if (lastTick+interval) < int(time.time() * 1000):
            print(values)

            if swarm != None:
                if not batteryChecked:
                    checkBattery()
                    batteryChecked = True
                    print("Battery: " + str(batteryVal))

                if all(i > 25 for i in batteryVal):
                    if int(values[1][0]) == 1 and not inFlight:
                        takeoffDrones()
                        print("Drone Takeoff!")
                        inFlight = True

                    if int(values[1][1]) == 1 and inFlight:
                        landDrones()
                        print("Landing Drones...")
                        inFlight = False

                    if int(values[1][2]) == 1:
                        iterateCounter()                   
                        lastChange = int(time.time() * 1000)
                        print("Counter Value: " + str(counter))
                    
                    if int(values[1][3]) == 1:
                        stopDrones()
                        disableControls()

                    if inFlight and not controlsDisabled:          
                        fb = values[0][0]
                        lr = values[0][1]
                        ud = values[0][2]
                        yaw = values[0][3]

                        sendControls(-fb, ud, lr, yaw, 30)

                else:
                    raise Exception("Battery Values Low - " + str(batteryVal))

            lastTick = int(time.time() * 1000)

    except Exception as e:
        running = False
        inFlight = False
        print("Error Caught: " + str(e) + " landing drones...")
        stopDrones()
        landDrones()



    
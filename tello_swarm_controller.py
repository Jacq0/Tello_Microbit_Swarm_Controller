from djitellopy import TelloSwarm
import serial_receive as sr
import time

#if the program is running or not
running = True
inFlight = False

#the time interval so we don't spam the drones with commands.
lastTick = int(time.time() * 1000) #time in millis
interval = 250

#the IP addresses of the tello drones
ips = ["192.168.1.3","192.168.1.4"]

swarm = TelloSwarm.fromIps(ips)
swarm.connect()

def landDrones():
    for drone in swarm:
        drone.land()

def takeoffDrones():
    for drone in swarm:
        drone.takeoff()

def sendControls(fb, ud, lr, yaw, speed):
    for drone in swarm:
        drone.send_rc_control(int(lr*speed), int(fb*speed), int(ud*speed), int(yaw*speed))

def stopDrones():
    for drone in swarm:
        drone.set_speed(0)

def flipForward():
    for drone in swarm:
        drone.flip_forward()

def flipBackwards():
    for drone in swarm:
        drone.flip_back()
    

while running:
    values = sr.returnInputValues()

    if (lastTick+interval) < int(time.time() * 1000):
        print(values)

        if int(values[1][0]) == 1 and not inFlight:
            takeoffDrones()
            inFlight = True

        if int(values[1][1]) == 1 and inFlight:
            #stopDrones()
            landDrones()
            inFlight = False
            running = False

        #if int(values[1][2]) == 1 and inFlight:
            #flipForward()
        
        #if int(values[1][3]) == 1 and inFlight:
            #flipBackwards()

        if inFlight:          
            fb = values[0][0]
            lr = values[0][1]
            ud = values[0][2]
            yaw = values[0][3]

            sendControls(fb, ud, lr, yaw, 50)

        lastTick = int(time.time() * 1000)



    
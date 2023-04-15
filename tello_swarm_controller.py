from djitellopy import TelloSwarm
import serial_receive as sr
import time

#if the program is running or not
running = True
inFlight = False

#the time interval so we don't spam the drones with commands.
lastTick = int(time.time() * 1000) #time in millis
interval = 100 

#the IP addresses of the tello drones
ips = ["192.168.1.63", "192.168.1.64"]

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
        drone.send_rc_control(lr*speed, fb*speed, ud*speed, yaw*speed)

def stopDrones():
    for drone in swarm:
        drone.set_speed(0)

while running:
    if (lastTick+interval) < int(time.time() * 1000):
        values = sr.returnInputValues()

        if values[4] == 1:
            takeoffDrones()
            inFlight = True

        if values[5] == 1:
            stopDrones()
            landDrones()
            inFlight = False
            running = False

        if inFlight:          
            fb = values[0]
            lr = values[1]
            ud = values[2]
            yaw = values[3]

            sendControls(fb, lr, ud, yaw, 5)
            lastTick = int(time.time() * 1000)



    
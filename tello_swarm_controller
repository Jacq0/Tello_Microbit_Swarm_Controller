from djitellopy import TelloSwarm
import serial_receive as sr

running = True

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
    values = sr.returnInputValues()

    if values[5] == 1:
        stopDrones()
        landDrones()
        running = False
    if values[4] == 1:
        takeoffDrones()

    fb = values[0]
    lr = values[1]
    ud = values[2]
    yaw = values[3]



    
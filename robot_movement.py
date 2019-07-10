# Autonomous indoor navigation robot
# Created by: Pong Loong Yeat, Calvin Low , Claire Jewel
# Date modified: 15/12/2018
# Dependencies: functions.py, motor.py, car_dir.py, main.py

# Import necessary libraries
from __future__ import division
import numpy as np
import math
from functions import *
import bluetooth
import time
from obstacle_avoidance import setupSensors
from sign_detection import try_image
from motor import setSpeed
from bluetooth import*
import pigpio

# Initialize servos and camera
setup_dir()
setup_servo()
setup_motor()
home()
init_signboard = 0
img_path = "/images/img.png"

# Initialisation ultrasonic sensor pin values
THRESHOLD = 37       # in cm
THRESHOLD_C = 35
THRESHOLD_OUT = 80

# Broadcom number
TRIG_PIN_L = 20
ECHO_PIN_L = 21

TRIG_PIN_C = 13
ECHO_PIN_C = 26

TRIG_PIN_R = 16
ECHO_PIN_R = 19
 
# GPIO number
# TRIG_PIN_L = 38
# ECHO_PIN_L = 40

# TRIG_PIN_C = 33
# ECHO_PIN_C = 37

# TRIG_PIN_R = 36
# ECHO_PIN_R = 35


UP_LIMIT = 1.02     # for getting stuck
LW_LIMIT = 0.98     # for getting stuck
STRAIGHT_SPEED = 38     # moving 'up'  and 'down' speed
TURN_SPEED = 40     # turning speed
sign_detect = 0     # If sign detected

# Initialising ultrasonic sensor readings
distance = setupSensors(TRIG_PIN_L, ECHO_PIN_L, TRIG_PIN_C, ECHO_PIN_C, TRIG_PIN_R, ECHO_PIN_R)
distance_l = distance[0]
distance_c = distance[1]
distance_r = distance[2]
distance_old_c = distance_c
distance_old_l = distance_l
distance_old_r = distance_r
print(distance)

data = ''   # Bluetooth data
client_socket = ''  # Client socket for bluetooth
dest = ''   # Robot destination


##################################################
# Description: Allows vehicle to reverse and     #
#              align itself to a wall.           #
# Input:                                         #
#        @sec: Float. Time in seconds for        #
#              vehicle to reverse and calibrate  #
#              itself.                           #
# Return: -                                      #
##################################################
def calibrateReverse(sec):
    global distance_r, distance_c, distance_l, distance_old_r, distance_old_c, distance_old_l
    stop()
    home()
    setSpeed(STRAIGHT_SPEED,STRAIGHT_SPEED)
    move('down')
    print('reverse')
    distance = setupSensors(TRIG_PIN_L, ECHO_PIN_L, TRIG_PIN_C, ECHO_PIN_C, TRIG_PIN_R, ECHO_PIN_R)
    distance_l = distance[0]
    distance_c = distance[1]
    distance_r = distance[2]
    start = time.time()
    end = time.time()
    while end - start < sec:
        if distance_r/distance_l > 1.0:
            move('down_right65')
            distance = setupSensors(TRIG_PIN_L, ECHO_PIN_L, TRIG_PIN_C, ECHO_PIN_C, TRIG_PIN_R, ECHO_PIN_R)
            distance_l = distance[0]
            distance_c = distance[1]
            distance_r = distance[2]
            print(distance)
            print('Calibrate left.')
        elif distance_r/distance_l < 1.0:
            move('down_left65')
            distance = setupSensors(TRIG_PIN_L, ECHO_PIN_L, TRIG_PIN_C, ECHO_PIN_C, TRIG_PIN_R, ECHO_PIN_R)
            distance_l = distance[0]
            distance_c = distance[1]
            distance_r = distance[2]
            print(distance)
            print('Calibrate right.')
        end = time.time()
    return


##################################################
# Description: Re-centres wheels.                 #
# Input: -                                       #
# Return: -                                      #
##################################################
def recentre():
    stop()
    home()
    return


##################################################
# Description: Execute signboard detection as    #
#			   robot encounter two possible path #
# Input: -                                       #
# Return: -                                      #
##################################################
def junction():
    global sign_detect
    error_ctr = 0 # count error
    error_check = 0 # error checking bit
    recentre()
    print("Please hold.")
    client_socket.send('4')
    error_check = try_image(dest, client_socket)
    while error_check == 1:
        if error_ctr == 2:
            calibrateReverse(1.5)
            error_ctr = 0
            break
        error_check = try_image(dest, client_socket)
        error_ctr += 1
    if error_check == 0:
        sign_detect = 1
    return


##################################################
# Description: Allows vehicle to turn left or    #
#              right.		                 #
# Input:                                         #
#        @direction: Str. String containing      #
#                    direction vehicle needs to  #
#                    turn.                       #
# Return: -                                      #
##################################################
def turning(direction):
    global distance_r, distance_c, distance_l, distance_old_r, distance_old_c, distance_old_l
    distance_old_c = distance_c
    distance_old_l = distance_l
    distance_old_r = distance_r
    distance = setupSensors(TRIG_PIN_L, ECHO_PIN_L, TRIG_PIN_C, ECHO_PIN_C, TRIG_PIN_R, ECHO_PIN_R)
    distance_l = distance[0]
    distance_c = distance[1]
    distance_r = distance[2]
    print(distance)
    # if distance_l/distance_old_l > LW_LIMIT and distance_l/distance_old_l < UP_LIMIT and distance_c/distance_old_c > LW_LIMIT and distance_c/distance_old_c < UP_LIMIT and distance_r/distance_old_r > LW_LIMIT and distance_r/distance_old_r < UP_LIMIT:
        # calibrateReverse(0.8)
    if distance_c < 10 and distance_old_c < 10:
        calibrateReverse(0.8)
    print('Turn ' + direction)
    move(direction)
    return


##################################################
# Description: Allows vehicle to head straight.  #
# Input: -                                       #
# Return: -                                      #
##################################################
def straight():
    global distance_r, distance_c, distance_l
    home()
    setSpeed(STRAIGHT_SPEED,STRAIGHT_SPEED)
    move('up')
    print("Keep moving forward.")
    
    while distance_r/distance_l > 1.0 and distance_r < THRESHOLD:
        move('right65')
        distance = setupSensors(TRIG_PIN_L, ECHO_PIN_L, TRIG_PIN_C, ECHO_PIN_C, TRIG_PIN_R, ECHO_PIN_R)
        distance_l = distance[0]
        distance_c = distance[1]
        distance_r = distance[2]
        print(distance)
        print('Calibrate right.')
    while distance_r/distance_l < 1.0 and distance_l < THRESHOLD:
        move('left65')
        distance = setupSensors(TRIG_PIN_L, ECHO_PIN_L, TRIG_PIN_C, ECHO_PIN_C, TRIG_PIN_R, ECHO_PIN_R)
        distance_l = distance[0]
        distance_c = distance[1]
        distance_r = distance[2]
        print(distance)
        print('Calibrate left.')
    return


##################################################
# Description: Initialises vehicle movement      #
#              and includes simple obstacle      #
#              avoiding logic.                   #
# Input: -                                       #
# Return: -                                      #
##################################################
def startMovement():
    global distance_r, distance_c, distance_l, distance_old_r, distance_old_c, distance_old_l, data, client_socket
    setSpeed(STRAIGHT_SPEED,STRAIGHT_SPEED)
    move('up')

    MAX_DIST = 350
    while data != 'BACK':
        client_socket.send('0')
        # try:
            # data = client_socket.recv(1024)
            # except socket.timeout:
            # print(data)
            # data = client_socket.recv(1024)
            # print(data)
        distance_old_c = distance_c
        distance_old_l = distance_l
        distance_old_r = distance_r
        distance = setupSensors(TRIG_PIN_L, ECHO_PIN_L, TRIG_PIN_C, ECHO_PIN_C, TRIG_PIN_R, ECHO_PIN_R)
        distance_l = distance[0]
        distance_c = distance[1]
        distance_r = distance[2]
        print(distance)

        if distance_l < THRESHOLD and distance_c < THRESHOLD_C and distance_r < THRESHOLD and distance_old_l < THRESHOLD and distance_old_c < THRESHOLD_C and distance_old_r < THRESHOLD:
            # Dead end/destination arrived
            recentre()
            setSpeed(STRAIGHT_SPEED,STRAIGHT_SPEED)
            move('up')
            if distance_l/distance_old_l > LW_LIMIT and distance_l/distance_old_l < UP_LIMIT and distance_c/distance_old_c > LW_LIMIT and distance_c/distance_old_c < UP_LIMIT and distance_r/distance_old_r > LW_LIMIT and distance_r/distance_old_r < UP_LIMIT:
                calibrateReverse(0.8)
                # print("You have arrived at your destination.")
                # break

        elif distance_l < THRESHOLD and distance_c >= THRESHOLD_C and distance_r < THRESHOLD and distance_old_l < THRESHOLD and distance_old_c >= THRESHOLD_C and distance_old_r < THRESHOLD:
            # Can only go straight
            straight()

        elif distance_l < THRESHOLD and distance_c < THRESHOLD_C and distance_r >= THRESHOLD and distance_old_l < THRESHOLD and distance_old_c < THRESHOLD_C and distance_old_r >= THRESHOLD:
            # Only right turn available
            client_socket.send('1')
            move('down')
            time.sleep(0.3)
            setSpeed(TURN_SPEED, TURN_SPEED)
            turning('right')
            time.sleep(1.0)
            while distance_r > THRESHOLD-10 or distance_old_r > THRESHOLD-10:
                setSpeed(TURN_SPEED-5, TURN_SPEED-5)
                turning('right')
                if distance_l < THRESHOLD and distance_c >= THRESHOLD and distance_r >= THRESHOLD and distance_old_l < THRESHOLD and distance_old_c >= THRESHOLD and distance_old_r >= THRESHOLD:
                    print('junction')
                    # move('right')
                    # time.sleep(0.3)
                    # home()
                    setSpeed(STRAIGHT_SPEED,STRAIGHT_SPEED)
                    move('up')
                    time.sleep(0.1)
                    break
                # if distance_l < THRESHOLD and distance_c < THRESHOLD_C and distance_r >= THRESHOLD_OUT and distance_old_l < THRESHOLD and distance_old_c < THRESHOLD and distance_old_r >= THRESHOLD_OUT:
                    # break
                if distance_l >= THRESHOLD_OUT and distance_c >= THRESHOLD_OUT and distance_r >= THRESHOLD_OUT and distance_old_l >= THRESHOLD_OUT and distance_old_c >= THRESHOLD_OUT and distance_old_r >= THRESHOLD_OUT:
                    break
                
        elif distance_l >= THRESHOLD and distance_c < THRESHOLD_C and distance_r < THRESHOLD and distance_old_l >= THRESHOLD and distance_old_c < THRESHOLD_C and distance_old_r < THRESHOLD:
            # Only left turn available
            client_socket.send('2')
            move('down')
            time.sleep(0.3)
            setSpeed(TURN_SPEED, TURN_SPEED)
            turning('left')
            time.sleep(0.5)
            while distance_l > THRESHOLD-10 or distance_old_l > THRESHOLD-10:
                setSpeed(TURN_SPEED+5, TURN_SPEED+5)
                turning('left')
                # if distance_l >= THRESHOLD_OUT and distance_c >= THRESHOLD_OUT and distance_r < THRESHOLD_OUT and distance_old_l >= THRESHOLD_OUT and distance_old_c >= THRESHOLD_OUT and distance_old_r < THRESHOLD_OUT:
                #   move('left')
                #   time.sleep(0.2)
                #   home()
                #   setSpeed(STRAIGHT_SPEED,STRAIGHT_SPEED)
                #   move('up')
                #   time.sleep(0.5)
                #   break
                if distance_l >= THRESHOLD_OUT and distance_c >= THRESHOLD_OUT and distance_r >= THRESHOLD_OUT and distance_old_l >= THRESHOLD_OUT and distance_old_c >= THRESHOLD_OUT and distance_old_r >= THRESHOLD_OUT:
                    break

        elif distance_l < THRESHOLD and distance_c >= THRESHOLD_C and distance_r >= THRESHOLD and distance_old_l < THRESHOLD and distance_old_c >= THRESHOLD_C and distance_old_r >= THRESHOLD:
            # Junction on front and right
            setSpeed(STRAIGHT_SPEED,STRAIGHT_SPEED)
            move('up')
            time.sleep(0.8)
            junction()
            
        elif distance_l >= THRESHOLD and distance_c < THRESHOLD_C and distance_r >= THRESHOLD and distance_old_l >= THRESHOLD and distance_old_c < THRESHOLD_C and distance_old_r >= THRESHOLD:
            # Junction on left and right
            setSpeed(STRAIGHT_SPEED,STRAIGHT_SPEED)
            move('down')
            time.sleep(0.5)
            junction()
            
        elif distance_l >= THRESHOLD and distance_c >= THRESHOLD_C and distance_r < THRESHOLD and distance_old_l >= THRESHOLD and distance_old_c >= THRESHOLD_C and distance_old_r < THRESHOLD:
            # Junction on front and left
            setSpeed(STRAIGHT_SPEED,STRAIGHT_SPEED)
            move('up')
            time.sleep(0.8)
            junction()

        elif distance_l >= THRESHOLD and distance_c >= THRESHOLD_C and distance_r >= THRESHOLD and distance_old_l >= THRESHOLD and distance_old_c >= THRESHOLD_C and distance_old_r >= THRESHOLD and sign_detect == 1:
            print('Open Space')
            client_socket.send('3')
            recentre()
            return
        
        else:
            recentre()
            setSpeed(STRAIGHT_SPEED-5,STRAIGHT_SPEED-5)
            move('up')
            if distance_l/distance_old_l > LW_LIMIT and distance_l/distance_old_l < UP_LIMIT and distance_c/distance_old_c > LW_LIMIT and distance_c/distance_old_c < UP_LIMIT and distance_r/distance_old_r > LW_LIMIT and distance_r/distance_old_r < UP_LIMIT:
                calibrateReverse(0.8)
            print('waiting')
           

##################################################
# Description: Connects to an application on a   #
#              device via Bluetooth to select    #
#              directory.                        #
# Input: -                                       #
# Return: -                                      #
##################################################
def bluetooth_connect():
    global data, client_socket, dest
    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    port = 1
    server_socket.bind(("", port))
    server_socket.listen(1)
    print 'Waiting for connection'
    try:
        client_socket, address = server_socket.accept()
        print "Accepted connection from ", address

    except Exception as e:
        print str(e)
        server_sock.close()
    server_socket.settimeout(0.1)
    while data != 'EXIT':
        try:
            data = client_socket.recv(1024)
        except bluetooth.btcommon.BluetoothError:
            print('Bluetooth: Error 1')
            break
        except KeyboardInterrupt:
            break
            
        print(data)
        if data != 'START':
            dest = data
            time.sleep(1)
            print(dest)
        else:
            try:
                startMovement()
            except KeyboardInterrupt:
                client_socket.send('3')
                break
            except bluetooth.btcommon.BluetoothError:
                print('Bluetooth: Error 2')
                break
            
        time.sleep(1)

    print 'Exit'
    data = ''
    client_socket.close()
    server_socket.close()
    recentre()
    return


if __name__ == '__main__':
    dest = 'CLASSROOM'
    data = 'START'
    
    while 1:
        sign_detect = 0
        bluetooth_connect()
        # startMovement()
        home()

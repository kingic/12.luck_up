#!/usr/bin/python

import smbus
import math
import time
from picamera import PiCamera
from time import sleep
import socket
import socketserver
from os.path import exists

HOST = '18.188.252.62'
PORT = 3000

camera = PiCamera()

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def getFileFromServer(filename):
        data_transferred = 0

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((HOST,PORT)) 
                print('file[%s] starting transmission...' %filename)
                filename = filename.encode()
                with open(filename, 'rb') as f:
                        try:
                                data = f.read(1024) 
                                while data: 
                                        data_transferred += sock.send(data)
                                        data = f.read(1024)
                        except Exception as e:
                                print(e)
 
        print('file[%s] finish transmission. transmission amount [%d]' %(filename, data_transferred))

def read_byte(adr):
	return bus.read_byte_data(address, adr)

def read_word(adr):

	high = bus.read_byte_data(address, adr)

	low = bus.read_byte_data(address, adr+1)

	val = (high << 8) + low

	return val

def read_word_2c(adr):
	val = read_word(adr)

	if (val >= 0x8000):

		return -((65535 - val) + 1)

	else :
		return val

def dist(a,b):

	return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):

	radians = math.atan2(x,dist(y,z))
	return -math.degrees(radians)

def get_x_rotation(x,y,z):

	radians = math.atan2(y,dist(x,z))
	return math.degrees(radians)

bus = smbus.SMBus(1)

address = 0x68

bus.write_byte_data(address, power_mgmt_1, 0)

i = 0
try:
	while True:

		time.sleep(1)
		print ("-------------------------------------")
		print ("=>gyro data")
		print ("-----------")
		gyro_xout = read_word_2c(0x43)
		gyro_yout = read_word_2c(0x45)
		gyro_zout = read_word_2c(0x47)
		print ("gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131))
		print ("gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131))
		print ("gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131))
		print ("=> accelerometer data")
		print ("--------------------")
		if gyro_xout < -1310 or gyro_xout > 1310:

			sleep(1)
			camera.capture('/home/pi/capston/capture' + str(i) +'.jpg')
			j = str(i)
			print ("caputured (" , i , ")")
			filename = "captured(" + j +")"
			getFileFromServer(filename)
			i = i+1
		accel_xout = read_word_2c(0x3b)
		accel_yout = read_word_2c(0x3d)
		accel_zout = read_word_2c(0x3f)
		accel_xout_scaled = accel_xout / 16384.0
		accel_yout_scaled = accel_yout / 16384.0
		accel_zout_scaled = accel_zout / 16384.0
		print ("accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled)
		print ("accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled)
		print ("accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled)
		print ("x rotation: ", get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
		print ("y rotation: ", get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
		print ("---------------------")

except KeyboardInterrupt:

	print ("program terminated")
	exit()



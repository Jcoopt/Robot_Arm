# -*- coding: utf-8 -*-
import smbus
import math
import time
import usb.core, usb.util, time,os,sys
import RPi.GPIO as GPIO
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)
GPIO.setup(27,GPIO.IN)
GPIO.setup(22,GPIO.IN)

#ARM SETUP
#allocate roboarm to device
RoboArm = usb.core.find(idVendor=0x1267, idProduct=0x0000)

#check if the arm is detected and warn if not
if RoboArm is None:
   raise ValueError("Arm not found")

#create a variable for duration
Duration=1

#Definne a procedure for execution of each movement
def MoveArm(Duration, ArmCmd):
    #start movement
    RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
    #stop movement after specified time
    time.sleep(Duration)
    ArmCmd=[0,0,0]
    RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,100)
#ARM SETUP COMPLETE


#GYRO+ACCELL SETUP
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
	else:
		return val
def dist(a,b):
	return math.sqrt((a*a)+(b*b))
def get_y_rotation(x,y,z):
	radians = math.atan2(x, dist(y,z))
	return -math.degrees(radians)
def get_x_rotation(x,y,z):
	radians = math.atan2(y, dist(x,z))
	return math.degrees(radians)
while True:
	try:
	        base=0
	        shol=0
		#bus = smbus.SMBus(0) #
		bus = smbus.SMBus(1) #for Revision 2 boards
		address = 0x68# This is the address value read via the i2cdetect command
		# Now wake the 6050 up as it starts in sleep mode
		bus.write_byte_data(address, power_mgmt_1, 0)
	##	print "gyro data"
	##	print "---------"
		gyro_xout = read_word_2c(0x43)
		gyro_yout = read_word_2c(0x45)
		gyro_zout = read_word_2c(0x47)
	#	print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
	##	print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
	##	print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)
	##	print
	##	print "accelerometer data"
	##	print "------------------"
		accel_xout = read_word_2c(0x3b)
		accel_yout = read_word_2c(0x3d)
		accel_zout = read_word_2c(0x3f)
		accel_xout_scaled = accel_xout / 16384.0
		accel_yout_scaled = accel_yout / 16384.0
		accel_zout_scaled = accel_zout / 16384.0
	#        print "accel_xout: ", round(accel_xout,1), " scaled: ", accel_xout_scaled,"accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled,"accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled
		print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
	#	print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled
	        #print "y",(gyro_yout/131),"z",(gyro_zout/131)
		print "x rotation: " , round(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled),1), "y rotation: " , round(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled),1)
	        xrot=round(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled),1)
	        yrot=round(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled),1)
	        while True:
	           if yrot <- 45:
	                   if (gyro_xout/131)>10:
	                      print "BIG X"
	                      MoveArm(0.5,[0,1,0])
	                      break
	                   else:
	                     break
	           elif  yrot>45:
	                   if (gyro_xout/131)<-10:
	                      print "SMALL X"
	                      MoveArm(0.5,[0,2,0])
	                      break
	                   else:
	                      break
	           elif xrot<-45:
	                   if (gyro_yout/131)>10:
	                      print "BIG Y"
	                      MoveArm(0.5,[32,0,0])
	                      break
	                   else:
	                      break
	           elif xrot >45:
	                   if (gyro_yout/131)<-10:
	                      print "SMALL Y"
	                      MoveArm(0.5,[16,0,0])
	                      break
	                   else:
	                      break
	           elif GPIO.input(17)==False:
			MoveArm(0.5,[2,0,0])
		   elif GPIO.input(27)==False:
			MoveArm(0.5,[1,0,0])
		   elif GPIO.input(22)==False:
			MoveArm(0.5,[0,0,1])
		   else:
	              break
	except IOError:
		base=0
   ##        if round(accel_xout,1)>15000:
   ##                print "big"
   ##                MoveArm(1,[2,0,0])
   ##        if round(accel_xout,1)<-15000:
   ##                print "small"
   ##                MoveArm(1,[1,0,0])
   ##        if base== 1:
   ##                MoveArm(0.5,[0,1,0])
   ##        if base==2:
   ##                  MoveArm(0.5,[0,2,0])
   ##        if shol== 1:
   ##                  MoveArm(0.5,[128,0,0])
   ##        if shol==2:
   ##                MoveArm(0.5,[64,0,0])
   ##	print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled
##                     base=0
##                     shol=0

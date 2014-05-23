#robot arm control program
#import the usb and time libraries
import usb.core, usb.util, time,pygame,os,sys
from pygame.locals import*

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
global base
global shol
base=0
shol=0
pygame.init()
screen = pygame.display.set_mode((68,60))
while True:
    #base
    if base>9:
        MoveArm(0.5,[0,2,0])
        base=base-1
    if base<-9:
        MoveArm(0.5,[0,1,0])
        base=base+1

        #sholder
        
    if shol>6:
        MoveArm(0.5,[64,0,0])
        shol=shol-1
    if shol<-6:
        MoveArm(0.5,[128,0,0])
        shol=shol+1
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            #base
            if event.key == K_d:
                MoveArm(0.5,[0,1,0])
                base=base+1
                print base 
            if event.key == K_a:
                MoveArm(0.5,[0,2,0])    
                base=base-1
                print base
            if event.key == K_p:
                base=0

           #shoulder    
            if event.key == K_w:
                MoveArm(0.5,[128,0,0])
                shol=shol+1
                print shol 
            if event.key == K_s:
                MoveArm(0.5,[64,0,0])    
                shol=shol-1
                print shol
            if event.key==K_l:
                shol=0
##MoveArm(1,[0,1,0])#rotate base anti-clockwise
##MoveArm(1,[0,2,0])#rotate base clockwise
##MoveArm(1,[64,0,0])#shoulder up
##MoveArm(1,[128,0,0])#shoulder down
##MoveArm(1,[16,0,0])#elbow up
##MoveArm(1,[32,0,0])#elbow down
##MoveArm(1,[4,0,0])#wrist up
##MoveArm(1,[8,0,0])#wrist down
##MoveArm(1,[2,0,0])#grip open
##MoveArm(1,[1,0,0])#grip close
##MoveArm(1,[0,0,1])#light on
##MoveArm(1,[0,0,0])#light off

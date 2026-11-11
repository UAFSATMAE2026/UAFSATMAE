import time
from roarm_ik import m2Arm
import pygame as pg
import serial as ser

def main():
    # Initializing our important variables
    
    pg.init() # initializing pygame for events so that our controller events will update as well
    serialCon = ser.Serial('/dev/ttyACM0', 115200)

    pg.joystick.init()
    joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
    print(joysticks)
    
    # arm = m2Arm(port = "/dev/ttyUSB0")
    # arm.move_init()

    alignment = 0
    latch = False
    
    clock = pg.time.Clock()
    
    # location of our arms gripper 
    xArmLoc = 0.0
    yArmLoc = 10.0
    zArmLoc = 10.0

    angle_grip = 10.0

    while(True):
        for event in pg.event.get():
            pass
        leftStickX = round( pg.joystick.Joystick(0).get_axis(0), 2 )  # rounding to 2 decimal spaces
        leftStickY = round( pg.joystick.Joystick(0).get_axis(1), 2 )

        if(pg.joystick.Joystick(0).get_button(7)): # button 7 is the start button on the xbox controller
            latch = not latch

            if latch:
                alignment = 1
            else:  
                alignment = 0

        x1_joystick = round( pg.joystick.Joystick(0).get_axis(2), 2) * -1
        y1_joystick = round( pg.joystick.Joystick(0).get_axis(3), 2) * -1

        if(pg.joystick.Joystick(0).get_hat(0)==(0,1)):  #control z axis movement
            zArmLoc = zArmLoc + .25
        elif(pg.joystick.Joystick(0).get_hat(0)==(0,-1)):
            zArmLoc = zArmLoc - .25

        if(pg.joystick.Joystick(0).get_hat(0)==(1,0)):  #control gripper angle
            angle_grip = angle_grip + .25
        elif(pg.joystick.Joystick(0).get_hat(0)==(-1,0)):
            angle_grip = angle_grip - .25

        if(x1_joystick > 0.25 or x1_joystick < -0.25):
            xArmLoc += x1_joystick
        if(y1_joystick > 0.25 or y1_joystick < -0.25):
            yArmLoc += y1_joystick
        
        serialCon.write(f'{leftStickX * 100} {leftStickY * 100} {alignment}'.encode("utf-8"))
        print(f"LSX: {leftStickX} LSY: {leftStickY} xArmLoc: {xArmLoc} yarm: {yArmLoc} zarm: {zArmLoc} alignment: {alignment} angle_grip: {angle_grip}")


        # arm.gripper_angle_ctrl(angle_grip, 10, 3)
        # arm.move_to_xyz(yArmLoc, xArmLoc, zArmLoc)
        clock.tick(60)

if __name__ == "__main__":
    main()

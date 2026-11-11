from roarm_ik import m2Arm
import pygame
import serial
import logging
from datetime import datetime
import sys

SERIAL_RATE = 115200

def main():
    # Initializing our logger, important for analyzing whats happening
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(f"logs/{ datetime.now().strftime('log_%Y-%m-%d_%H-%M-%S.log') }", mode="w"),
            logging.StreamHandler(sys.stdout)
        ])
    logger = logging.getLogger(__name__)
    
    # Initializing our modules
    pygame.init() # Initializes pygame, our module we use for recording controller input
    pygame.joystick.init() # Initializes the controller reading portion of pygame

    # Initializing our arm 
    try:
        arm = m2Arm() # defaults to /dev/ttyUSB0
        arm.move_init()
    except serial.SerialException as e: # Setting arm to None if no arm is connected.
        arm = None
        logger.critical("Arm not connected. Setting to null from this point forward.")
        
    # Initializing our important variables
    if pygame.joystick.get_count() == 0:
        logger.info("Waiting for controller to connect...")
        while pygame.joystick.get_count() == 0: pass
    controller = pygame.joystick.Joystick(0) # sets the first controller to the controller variable. we will only ever connect 1 controller to the jetson.

    alignment = False # Differentiates between robot tank movement and car movement
    clock = pygame.time.Clock() 

    # Initializing controller joystick value variables
    leftStickX = None
    leftStickY = None
    rightStickX = None
    rightStickY = None

    # Location of our arms gripper 
    xArmLoc = 0.0
    yArmLoc = 10.0
    zArmLoc = 10.0
    gripperAngle = 10.0

    logger.info("Connecting to Arduino...")
    try:
        with serial.Serial('/dev/ttyACM0', SERIAL_RATE) as ser:
            logger.info(f"Connection successful! Connect with rate {SERIAL_RATE}")
            while True:
                    logger.info("Clearing pygame event queue...")
                    pygame.event.clear() # Emptying event queue to continue reading

                    # Getting values of the L and R joysticks
                    leftStickX = round(controller.get_axis(0), 2) * 100
                    leftStickY = round(controller.get_axis(1), 2) * 100

                    rightStickX = round(controller.get_axis(2), 2) * -1
                    rightStickY = round(controller.get_axis(3), 2) * -1

                    if controller.get_button(7): # Swapping between robot tank movement and car movement with XBOX Menu Button
                        alignment = not alignment

                    if controller.get_hat(0) == (0, 1): # Control Arm Z-Axis Movement
                        zArmLoc += 0.25
                    elif controller.get_hat(0) == (0, -1):
                        zArmlock -= 0.25
                    
                    if controller.get_hat(0) == (1, 0): # Control Gripper
                        gripperAngle += 0.25
                    elif controller.get_hat(0) == (-1, 0):
                        gripperAngle -= 0.25
                    
                    # Utilizing my Discrete Math knowledge to check if the right joystick is in the deadzone or not
                    if not (rightStickX < 0.25 and rightStickX > -0.25):
                        xArmLoc += rightStickX
                    if not (rightStickY < 0.25 and rightStickY > -0.25):
                        yArmLoc += rightStickY

                    # Sending off data to the arm and Arduino
                    ser.write(f"{leftStickX} {leftStickY} {int(alignment)}".encode("utf-8"))
                    arm.move_to_xyz(yArmLoc, xArmLoc, zArmLoc)
                    arm.gripper_angle_ctrl(gripperAngle, 10, 3)
                    # No point in logging this data as it will just flood the logs, so I'm just gonna have it print.
                    print(f"""LSX: {leftStickX} LSY: {leftStickY}
                        xArmLoc: {xArmLoc} yArmLoc: {yArmLoc} zarm: {zArmLoc}
                        alignment: {int(alignment)} Gripper Angle: {angle_grip}""")
                    
                    clock.tick(60)
    except serial.SerialException as e:
        logger.error(f"An exception has occurred with the serial! {e}", exc_info=True)
    except Exception as e:
        logger.error(f"An unknown exception has occurred! {e}, exc_info=True")


if __name__ == "__main__":
    main()
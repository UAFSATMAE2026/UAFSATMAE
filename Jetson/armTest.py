from roarm_ik import m2Arm

# Initializing our arm 
try:
    arm = m2Arm() # defaults to /dev/ttyUSB0
    arm.move_init()
except serial.SerialException as e: # Setting arm to None if no arm is connected.
    arm = None

if pygame.joystick.get_count() == 0:
    logger.info("Waiting for controller to connect...")
    while pygame.joystick.get_count() == 0: pass
controller = pygame.joystick.Joystick(0) # sets the first controller to the controller variable. we will only ever connect 1 controller to the jetson.

clock = pygame.time.Clock() 

# Location of our arms gripper 
xArmLoc = 0.0
yArmLoc = 10.0
zArmLoc = 10.0
gripperAngle = 10.0



while True:
    rightStickX = round(controller.get_axis(2), 2) * -1
    rightStickY = round(controller.get_axis(3), 2) * -1
    
    if controller.get_hat(0) == (0, 1): # Control Arm Z-Axis Movement
        zArmLoc += 0.25
    elif controller.get_hat(0) == (0, -1):
        zArmloc -= 0.25
    
    if controller.get_hat(0) == (1, 0): # Control Gripper
        gripperAngle += 0.25
    elif controller.get_hat(0) == (-1, 0):
        gripperAngle -= 0.25
    
    if not (rightStickX < 0.25 and rightStickX > -0.25):
        xArmLoc += rightStickX
    if not (rightStickY < 0.25 and rightStickY > -0.25):
        yArmLoc += rightStickY

    arm.move_to_xyz(yArmLoc, xArmLoc, zArmLoc)
    arm.gripper_angle_ctrl(gripperAngle, 10, 3)
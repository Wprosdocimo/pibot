import pygame #Import Modules
import usb.core
import time
pygame.init()#Initialize pygame

# Wait for a joystick
while pygame.joystick.get_count() == 0:
  print 'waiting for joystick count = %i' % pygame.joystick.get_count()
  time.sleep(10)
  pygame.joystick.quit()
  pygame.joystick.init()

j = pygame.joystick.Joystick(0)
j.init()#Initialize Joystick

print 'Initialized Joystick : %s' % j.get_name()#Print joystick if present

armFound = False

while not armFound: #Find Robot Arm
  dev = usb.core.find(idVendor=0x1267, idProduct=0x0000)

  if dev is None:#If Robot Arm not found, alert user
    print 'Arm not found. Waiting'
    time.sleep(10)
  else:
    armFound = True
#this arm should just have one configuration
dev.set_configuration()

#Print Controls to user
print("")
print("Joysticks:")
print("LEFT JOY UP/DOWN:    SHOULDER UP/DOWN")
print("LEFT JOY LEFT/RIGHT: BASE CLOCKWISE/ANTICLOCKWISE")
print("RIGHT JOY UP/DOWN:   ELBOW UP/DOWN")
print("R1: WRIST UP")
print("R2: WRIST DOWN")
print("X:  GRIP OPEN")
print("O:  GRIP CLOSE")
print("SELECT: TOGGLE LIGHT ON/OFF")
print("")
print("To Close, press 'Ctrl + C'")

# How far to move the JoyStick before it has an effect (0.60 = 60%)
threshold = 0.50#Sensitivity

# Key mappings
PS3_BUTTON_SELECT = 0


PS3_AXIS_LEFT_HORIZONTAL = 0
PS3_AXIS_LEFT_VERTICAL = 1
PS3_AXIS_RIGHT_HORIZONTAL = 2
PS3_AXIS_RIGHT_VERTICAL = 3
PS3_AXIS_X = 17
PS3_AXIS_CIRCLE = 18
PS3_AXIS_R1 = 15
PS3_AXIS_R2 = 13

# Robot Arm  defaults
Command = (0,0,0)
lightonoff = 0
shoulder = 0
base = 0
elbow = 0
wristup = 0
wristdown = 0
grip_open = 0
grip_close = 0
grip_command = 0
wrist_command = 0
shoulder_command = 0
base_command = 0
elbow_command = 0
           
 # ARM control
def SetCommand(axis_val):#Returns number depending on axis value
    if axis_val > threshold:
        return 1
    elif axis_val < -threshold:
        return 2
    elif abs(axis_val) < threshold:
        return 0


def BuildCommand(shoulc,basec,elbowc,wristc,gripc,lightc):#Builds Command
    byte1 = shoulc + elbowc +  wristc + gripc#Combines instructions for byte1
    list1 = [str(shoulc), str(elbowc), str(wristc), str(gripc), str(basec), str(lightc)]#Compiles commands into 1 command
        
def ProcessArm(event):#Detects input and processes
      global Command, lightonoff, shoulder, base, elbow, wristup, wristdown, grip_open, grip_close, grip_command, wrist_command, shoulder_command, base_command, elbow_command
     
      if event.type == pygame.JOYBUTTONDOWN:
          if event.button == PS3_BUTTON_SELECT:
            if lightonoff == 0:
              lightonoff = 1
            else:
              lightonoff = 0
      elif event.type == pygame.JOYAXISMOTION:
        if event.axis == PS3_AXIS_LEFT_VERTICAL:
          shoulder = event.value
        elif event.axis == PS3_AXIS_LEFT_HORIZONTAL:
          base = event.value
        elif event.axis == PS3_AXIS_RIGHT_VERTICAL:         
          elbow = event.value
        elif event.axis == PS3_AXIS_R1:   
          wristup = event.value
        elif event.axis == PS3_AXIS_R2:
          wristdown = event.value
        elif event.axis == PS3_AXIS_X:         
          grip_open = event.value
        elif event.axis == PS3_AXIS_CIRCLE:         
          grip_close = event.value

        # Open/Close Gripper?
        if grip_open > threshold:
            grip_command = 1
        elif grip_close > threshold:
            grip_command = 2
        else:
            grip_command = 0
       
       
        # Wrist Up/Down?
        if wristup > threshold:
            wrist_command = 1*4
        elif wristdown > threshold:
            wrist_command = 2*4
        else:
            wrist_command = 0

        #Produces final command for each 'body' part
        shoulder_command = SetCommand(shoulder)*64
        base_command = SetCommand(base)
        elbow_command = SetCommand(elbow)*16
       
        # Work out what to send out to the robot
        NewCommand = BuildCommand(shoulder_command,base_command,
                                  elbow_command, wrist_command, grip_command,lightonoff)
                                 
        # If the command has changed, send out the new one
        if NewCommand != Command:
            dev.ctrl_transfer(0x40, 6, 0x100, 0, NewCommand, 1000)
            Command = NewCommand
try:
    # Loop forever
    while True:
        time.sleep(0.1)#time.sleep(0.1)
       
        # read in events
        events = pygame.event.get()
              
        # and process them
        for event in events:
            ProcessArm(event)
except KeyboardInterrupt:
    j.quit()#End joystick input
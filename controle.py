import RPi.GPIO as GPIO			#importando bibliotecas
from gpiozero import Robot
import time
import getch

# GPIO.setmode(GPIO.BOARD)		
# GPIO.setwarnings(False)

# F_DIREITA = 16				# mapeamento dos motores
# F_ESQUERDA = 11
# T_DIREITA = 18
# T_ESQUERDA = 13

robot = Robot(left=(17, 27), right=(23, 24))

# def setup_motor():			# setup do motor
    # GPIO.setup(F_DIREITA,GPIO.OUT)
    # GPIO.setup(F_ESQUERDA,GPIO.OUT)
    # GPIO.setup(T_DIREITA,GPIO.OUT)
    # GPIO.setup(T_ESQUERDA,GPIO.OUT)

def move_frente():			# move para frente
    robot.forward(0.4)
    # GPIO.output(F_DIREITA,GPIO.HIGH)
    # GPIO.output(F_ESQUERDA,GPIO.HIGH)
    # time.sleep(0.4)
    # GPIO.output(F_DIREITA,GPIO.LOW)
    # GPIO.output(F_ESQUERDA,GPIO.LOW)

def move_tras():			# move para tras
    robot.backward()
    # GPIO.output(T_DIREITA,GPIO.HIGH)
    # GPIO.output(T_ESQUERDA,GPIO.HIGH)
    # time.sleep(0.4)
    # GPIO.output(T_DIREITA,GPIO.LOW)
    # GPIO.output(T_ESQUERDA,GPIO.LOW)
    
def move_direita():			#move para direita
    robot.right()
    # GPIO.output(F_ESQUERDA,GPIO.HIGH)
    # time.sleep(0.2)
    # GPIO.output(F_ESQUERDA,GPIO.LOW)

def move_esquerda():			#move para esquerda
    robot.left()
    # GPIO.output(F_DIREITA,GPIO.HIGH)
    # time.sleep(0.2)
    # GPIO.output(F_DIREITA,GPIO.LOW)

def move_parar():			#PARA tudo !
    robot.forward()
    # GPIO.output(T_DIREITA,GPIO.LOW)
    # GPIO.output(T_ESQUERDA,GPIO.LOW)
    # GPIO.output(F_DIREITA,GPIO.LOW)
    # GPIO.output(F_ESQUERDA,GPIO.LOW)
    
def le_tecla():				#leitura do teclado
    while True:
        tecla_comando = getch.getch()
        if tecla_comando == 'w':
            move_frente()
        elif tecla_comando == 's':
            move_tras()
        elif tecla_comando == 'd':
            move_direita()
        elif tecla_comando == 'a':
            move_esquerda()
        elif tecla_comando == 'q':
            move_parar()


# setup_motor()
le_tecla()

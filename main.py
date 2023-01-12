from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLE import *
from OpenGL.GLUT import * 
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *
from mallet import *
from puck import *
import sys

import socket
import numpy as np
import time
import base64
#import threading, wave, pyaudio,pickle,struct
import threading, wave, pickle,struct
import sys
import queue
import os
# For details visit pyshine.com
q = queue.Queue(maxsize=10)



BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
#host_ip = '192.168.1.1'#  socket.gethostbyname(host_name)
host_ip = '192.168.97.153'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9699
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)

"""
EQUIPO 5:
Jonathan Canales Puga
Nubia Esmeralda Cantú Sánchez
Jose Andrik Martinez Rodriguez
Hector Javier Morales Alanis
Jorge Jhovan Rodriguez Moreno

"""


class mesa(QMainWindow):
    def __init__(self, parent=None):
        """
        Constructor de la clase principal del proyecto, se colocan los atributos y características 
        de la mesa.

        """
        super(mesa, self).__init__()
        #Dimensiones de la mesa
        self.SCREEN_WIDTH=480
        self.SCREEN_HEIGHT=480
        self.TABLE_WIDTH = 2.0 #x
        self.TABLE_HEIGHT = 4.0 #y
        self.TABLE_LENGTH = 4.0 #z
        self.mat_diffuse=[1.0, 1.0, 1.0, 0.0]
        self.light_ambient=[0.5, 0.5, 0.5, 1.0]
        self.light_diffuse=[1.0, 1.0, 1.0, 1.0]
        self.posiciones=[]
        self.MAX_X_ANGLE = 30.0
        self.MIN_X_ANGLE = 0.0
        self.lista=[]
        self.GOAL_LENGTH = 0.8
        self.WALL_THICK = 0.1
        self.WALL_HEIGHT = 0.1
        self.PUCK_DIAMETER = 0.2
        self.PUCK_HEIGHT = 0.1
        self.MALLET_DIAMETER = 0.3
        self.MALLET_HEIGHT = 0.1

        self.eye=[0.0, self.TABLE_HEIGHT * 1.5, 6.0]
        self.to=[0.0, 0, -self.TABLE_LENGTH / 2.0 ]
        self.up=[0.0, 3.0, -1.0]

        self.MAX_X_ANGLE = 30.0
        self.MIN_X_ANGLE = 0.0

        self.GOAL_LENGTH = 0.8

        self.WALL_THICK = 0.1
        self.WALL_HEIGHT = 0.1
        #Angulos de vision de la mesa
        self.xAngle=0.0
        self.yAngle=0.0
        self.bandera_movimiento=0
        self.MAX_MALLET_X = (self.TABLE_WIDTH - self.MALLET_DIAMETER) / 2
        self.MIN_MALLET_X = - self.MAX_MALLET_X
        self.MAX_MALLET_Z = (self.TABLE_LENGTH - self.MALLET_DIAMETER) / 2
        self.MIN_MALLET_Z = (self.MALLET_DIAMETER) / 2
        self.movimiento=None
        #Instancias a las clase de los jugadores y Puck
        self.puck = Puck()
        self.player = mallet()
        self.aiPlayer = mallet()
        self.x_position=0
        self.y_position=self.TABLE_HEIGHT / 2
        self.z_position=self.TABLE_LENGTH / 2 - self.MALLET_DIAMETER

        self.player2X=0
        self.player2Y=self.TABLE_HEIGHT / 2
        self.player2Z=self.MALLET_DIAMETER - self.TABLE_LENGTH / 2

        self.difference_x=0
        self.difference_z=0
        self.gameEnd=0

        self.goalred = 0
        self.goalblue = 0
        self.marcadorred = str(self.goalred) 
        self.marcadorblue = str(self.goalblue) 
        self.i = 1

        t1 = threading.Thread(target=self.get_message, args=())
        t2= threading.Thread(target=self.send_message, args=())
        t1.start()
        t2.start()
        
    def glInit(self):
        """
        Metodo para inicializar la interfaz en donde se colocará la mesa del juego.
        Implementando los atributos de la misma.
        """
        glClearColor(1.0, 1.0, 1.0, 0.0)
        
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)

        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.mat_diffuse)

        glLightfv(GL_LIGHT1, GL_AMBIENT, self.light_ambient)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, self.light_diffuse)
        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT1)
        glEnable(GL_AUTO_NORMAL)
        glEnable(GL_NORMALIZE)
        glEnable(GL_COLOR_MATERIAL)   

    def drawCube(self,x,y,z):
        """
        Método para dibujar cubos para realizar la mesa del juego.

        Args: Coordenadas x,y,z donde se posicionará el cubo en el plano
        """
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glScaled(x, y, z)
        glutSolidCube(1.0)
        glPopMatrix()

    def gameInit(self):
        """
        Método para inicializar los jugadores y el puck en el juego (mesa).
        Colocando sus respectivos colores y dimensiones.
        """
        self.aiPlayer=mallet()
        self.aiPlayer.setColor(0.7,0.2,0.2)
        self.aiPlayer.setParameter(self.MALLET_DIAMETER / 2,self.MALLET_HEIGHT)

        self.player = mallet()
        self.player.setColor(0.2,0.2,1.0)
        self.player.setParameter(self.MALLET_DIAMETER / 2, self.MALLET_HEIGHT)
        self.puck=Puck()
        self.puck.setColor(0.1,0.0,0.1)
        self.puck.setParameter(self.PUCK_DIAMETER / 2,self.PUCK_HEIGHT)

    def drawWall(self):
        """
        Función para generar las paredes de la mesa en el proyecto.
        Se colocan los colores y las posiciones de cada una de las paredes de la mesa.
        """
        #// Left Wall
        glPushMatrix()
        #// table wall on the ground
        glColor3d(0.2, 0.2, 0.2)
        glTranslated( (self.TABLE_WIDTH + self.WALL_THICK)/2.0, 0, 0)
        self.drawCube(self.WALL_THICK, self.TABLE_HEIGHT, self.TABLE_LENGTH)
        #// table edge on the wall
        glColor3d(0.6, 0.6, 0.6)
        glTranslated(0.0, (self.TABLE_HEIGHT + self.WALL_THICK) / 2.0, 0.0)
        self.drawCube(self.WALL_THICK, self.WALL_THICK, self.TABLE_LENGTH)
        glPopMatrix()

        glPushMatrix()
        #// table wall on the ground
        glColor3d(0.2, 0.2, 0.2)
        glTranslated(-(self.TABLE_WIDTH + self.WALL_THICK) / 2.0, 0, 0)
        self.drawCube(self.WALL_THICK, self.TABLE_HEIGHT, self.TABLE_LENGTH)
        #// table edge on the wall
        glColor3d(0.6, 0.6, 0.6)
        glTranslated(0, (self.TABLE_HEIGHT + self.WALL_THICK) / 2.0, 0)
        self.drawCube(self.WALL_THICK, self.WALL_THICK, self.TABLE_LENGTH)
        glPopMatrix()

        #// length of wall beside the goal
        length = (self.TABLE_WIDTH - self.GOAL_LENGTH) / 2.0 + self.WALL_THICK

        glPushMatrix()
        #// table wall on the ground
        glColor3d(0.2, 0.2, 0.2)
        glTranslated(0, 0, (self.TABLE_LENGTH + self.WALL_THICK) / 2.0)
        self.drawCube(self.TABLE_WIDTH + 2 * self.WALL_THICK, self.TABLE_HEIGHT, self.WALL_THICK)
        #// table edge on the wall with Goal
        glColor3d(0.6, 0.6, 0.6)
        glTranslated((self.GOAL_LENGTH + length)/2, (self.TABLE_HEIGHT + self.WALL_THICK) / 2.0, 0)
        self.drawCube(length, self.WALL_THICK, self.WALL_THICK)
        glTranslated(-(self.GOAL_LENGTH + length), 0, 0)
        self.drawCube(length, self.WALL_THICK, self.WALL_THICK)
        glPopMatrix()

        glPushMatrix()
        #// table wall on the ground
        glColor3d(0.2, 0.2, 0.2)
        glTranslated(0, 0, -(self.TABLE_LENGTH + self.WALL_THICK) / 2.0)
        self.drawCube(self.TABLE_WIDTH + 2 * self.WALL_THICK, self.TABLE_HEIGHT, self.WALL_THICK)
        #// table edge on the wall with Goal
        glColor3d(0.6, 0.6, 0.6)
        glTranslated((self.GOAL_LENGTH + length)/2, (self.TABLE_HEIGHT + self.WALL_THICK) / 2.0, 0)
        self.drawCube(length, self.WALL_THICK, self.WALL_THICK)
        glTranslated(-(self.GOAL_LENGTH + length), 0, 0)
        self.drawCube(length, self.WALL_THICK, self.WALL_THICK)
        glPopMatrix()

        glPushMatrix()
        #// table center
        glColor3d(0.6, 0.6, 0.6)
        glTranslated((self.GOAL_LENGTH + length)/2, (self.TABLE_HEIGHT + self.WALL_THICK) / 2.0-0.095, 0)
        self.drawCube(length, self.WALL_THICK, self.WALL_THICK)
        glTranslated(-(self.GOAL_LENGTH + length), 0, 0)
        self.drawCube(length, self.WALL_THICK, self.WALL_THICK)
        glPopMatrix()
        
    def drawTable(self):
        """
        Función para dibujar la mesa o la superficie de esta misma en el proyecto.
        """
        glPushMatrix()
        glColor3d(0.2, 0.7, 0.2)
        self.drawCube(self.TABLE_WIDTH, self.TABLE_HEIGHT, self.TABLE_LENGTH)
        glPopMatrix()

    def gameRestart(self):
        """
        Método para reiniciar el juego. Colocando las posiciones de cada uno de los objetos del
        proyecto en sus posiciones iniciales.
        """
        gameEnd=0
        self.aiPlayer.setPosition(0, self.TABLE_HEIGHT / 2, self.MALLET_DIAMETER - self.TABLE_LENGTH / 2)
        self.player.setPosition(0, self.TABLE_HEIGHT / 2, self.TABLE_LENGTH / 2 - self.MALLET_DIAMETER)
        self.puck.setPosition(0, self.TABLE_HEIGHT / 2, 0)

    def send_message(self):
        s = socket.socket()
        s.bind((host_ip, (port-1)))
        s.listen(5)
        client_socket,addr = s.accept()
        cnt=0
        while True:
            if client_socket:
                while True:
                    print('SERVER TEXT SENDING:')
                    #data = input ()
                    a = pickle.dumps(self.posiciones)
                    message = struct.pack("Q",len(a))+a
                    client_socket.sendall(message)
                    cnt+=1

    def get_message(self):
        s = socket.socket()
        s.bind((host_ip, (port-2)))
        s.listen(5)
        client_socket,addr = s.accept()
        data = b""
        payload_size = struct.calcsize("Q")

        while True:
            try:
                while len(data) < payload_size:
                    packet = client_socket.recv(4*1024) # 4K
                    if not packet: break
                    data+=packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q",packed_msg_size)[0]
                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data  = data[msg_size:]
                frame = pickle.loads(frame_data)
                self.lista=frame
                self.jugador()
                #self.aiPlayer.setPosition(frame[0],frame[1],frame[2])
                #print('',end='\n')
                #print('CLIENT TEXT RECEIVED:',frame,end='\n')
                #print('SERVER TEXT SENDING:')

            except Exception as e:
                print(e)
                pass

        client_socket.close()
        print('Audio closed')

    def jugador(self):
        if len(self.lista)>0:
            print(self.lista[0],self.lista[1],self.lista[2])
            self.aiPlayer.setPosition(self.lista[0],self.lista[1],self.lista[2])

    def display(self):
        """
        Método para mostrar todos los objetos del proyecto en la interfaz.
        Mesa, paredes, jugadores y puck.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        
        glLoadIdentity()
        gluLookAt(self.eye[0], self.eye[1], self.eye[2], self.to[0], self.to[1], self.to[2], self.up[0], self.up[1], self.up[2])
        glRotatef(self.yAngle, 0, 1, 0)
        glRotatef(self.xAngle, 1, 0, 0)
        self.drawTable()
        self.drawWall()
        #Se colocan los puntajes para cada jugador
        self.drawScore(400, 450, (1, 0, 0), "Red: "+self.marcadorred)
        self.drawScore(395, 10, (0, 0.1, 1), "Blue: "+self.marcadorblue)

        #Se dibujan los jugadores en la mesa.
        self.player.draw()
        self.aiPlayer.draw()
        self.puck.draw()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(35, self.SCREEN_WIDTH / self.SCREEN_HEIGHT, 1, 100)
        glFlush()
        glutSwapBuffers()
    
    def drawScore(self, x, y, color, text):  
        #Mostrar el Score del juego en una respectiva posición dentro de la interfaz
        glColor3fv(color)
        glWindowPos2f(x, y)
        glutBitmapString(GLUT_BITMAP_TIMES_ROMAN_24, text.encode('ascii'))

    def keyInput(self, key,x,y):
        """
        Función para establecer las teclas para los movimientos del primer jugador.
        Y posicionar la ficha de acuerdo a los movimientos.
        """
        if key == GLUT_KEY_RIGHT:
            if(self.x_position<0.79):
                self.x_position+=0.1
                self.posiciones=[self.x_position,self.y_position,self.z_position]
                self.player.setPosition(self.x_position,self.y_position,self.z_position)
                #self.send_message(self.posiciones)
                print(self.x_position,self.y_position,self.z_position)
                glutPostRedisplay()
            return
        elif key == GLUT_KEY_LEFT:
            if(self.x_position>-0.79):
                self.x_position-=0.1
                self.posiciones=[self.x_position,self.y_position,self.z_position]
                self.player.setPosition(self.x_position,self.y_position,self.z_position)
                #self.send_message(self.posiciones)
                print(self.x_position,self.y_position,self.z_position)

                glutPostRedisplay()
            return
        elif key == GLUT_KEY_UP:
            if self.z_position>0+self.PUCK_DIAMETER:
                self.z_position-=0.1
                self.posiciones=[self.x_position,self.y_position,self.z_position]
                self.player.setPosition(self.x_position,self.y_position,self.z_position)
                #self.posiciones=[self.x_position,self.y_position,self.z_position]
                print(self.x_position,self.y_position,self.z_position)

                #self.send_message(self.posiciones)
                glutPostRedisplay()
            return
        elif key == GLUT_KEY_DOWN:
            length = (self.TABLE_WIDTH - self.GOAL_LENGTH) / 2.0 + self.WALL_THICK
            if self.z_position<1.8:
                self.z_position+=0.1
                self.posiciones=[self.x_position,self.y_position,self.z_position]
                print(self.x_position,self.y_position,self.z_position)
                self.player.setPosition(self.x_position,self.y_position,self.z_position)
                #self.send_message(self.posiciones)
                glutPostRedisplay()
                return

    def NormalkeyInput(self, key,x,y):
        """
        Método para establecer las teclas para los movimientos del segundo jugador y los movimientos
        de perspectiva de la mesa.
        """
        key = key.decode("utf-8")
        #Movimientos de cambio de perspectiva de la mesa
        if key == 'x':
            self.xAngle+=0.5
            glutPostRedisplay()
            return

        if key == 'z':
            self.yAngle+=0.5
            glutPostRedisplay()
            return

        if key == 'c':
            self.xAngle-=0.5
            glutPostRedisplay()
            return

        if key == 'v':
            self.yAngle-=0.5
            glutPostRedisplay()
            return

    def reshape(self,width,height):
        """
        Método para establecer ancho y alto de la mesa.
        """
        glViewport(0, 0,width,height)
        if(height == 0):
            height = 1 
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(35, width / height, 0.1, 30) 

    def collide(self,x,z,radius):
        """
        Método para obtener las colisiones entre los objetos dentro del juego.
        """
        equis=x
        zeta=z
        if(abs(equis-self.puck.x)+abs(zeta-self.puck.z)<self.puck.getRadius()+radius):
            return True
        else:
            return False

    def restartScore(self):
        #Método para reiniciar los puntajes al momento de que un jugador gane el juego
        self.goalred = 0
        self.goalblue = 0
        self.marcadorred = str(self.goalred) 
        self.marcadorblue = str(self.goalblue) 

    def score (self, x, z): 
        #Funcion para agregar los goles a la ventana
        if (z == 1.8) and (x >= -0.4 and x <= 0.4) :
            self.goalred += 1 
            self.marcadorred=str(self.goalred)

            #Condicion para reiniciar el juego
            if self.goalred == 5:
                text= "El jugador Rojo ha sido el ganador"
                QMessageBox.warning(self,"Victoria!",text,QMessageBox.Ok)
                self.bandera_movimiento = False
                self.restartScore()
                self.gameRestart()
        elif (z == -1.8) and (x >= -0.4 and x <= 0.4) :
            self.goalblue += 1
            self.marcadorblue=str(self.goalblue)
            #Condicion para reiniciar el juego
            if self.goalblue == 5:
                text= "El jugador Azul ha sido el ganador"
                QMessageBox.warning(self,"Victoria!",text,QMessageBox.Ok)
                self.bandera_movimiento = False
                self.restartScore()
                self.gameRestart()

    def collideWall(self,x,z):
        """
        Método para establecer las colisiones del puck en las paredes de la mesa.

        Args: Coordenadas x y z del Puck
        """
        x=round(x,1)
        z=round(z,1)
        #Condicion para la bandera de los scores, ya que se repite dos veces 1.8 y -1.8
        if (z == 1.8) or (z == -1.8):
            if self.i == 1:
                self.score(x,z)
                self.i += 1
            else:
                self.i = 1

        if(x==-0.80 and z==-1.8):
            return 1
        elif(x>-0.80 and x<0.89 and z==-1.8):
            return 2
        elif(x==0.80 and z==-1.8):
            return 3
        elif(x==0.80 and (z>-1.8 and z<1.8)):
            return 4
        elif(x==0.80 and z==1.8):
            return 5
        elif(x>-0.80 and x<0.89 and z==1.8):
            return 6
        elif(x==-0.80 and z==1.8):
            return 7
        elif(x==-0.80 and (z>-1.8 and x<1.8)):
            return 8
        else:
            return 0

    def onTimer(self,timer):
        """
        Método Timer para actualizar constantemente los movimientos del puck y las 
        colisiones de este mismo
        """
        #Condición para esperar la primera colisión
        if self.bandera_movimiento:
            self.puck.move(self.movimiento,self.difference_x,self.difference_z)

        if (self.collide(self.player.x, self.player.z,self.player.getRadius())==True):
            self.bandera_movimiento=1
            self.movimiento=True
            self.difference_x=self.puck.x-self.player.x
            self.difference_z=self.puck.z-self.player.z

        elif(self.collide(self.aiPlayer.x, self.aiPlayer.z,self.aiPlayer.getRadius())==True):
            self.bandera_movimiento=1
            self.movimiento=False
            self.difference_x=self.puck.x-self.aiPlayer.x
            self.difference_z=self.puck.z-self.aiPlayer.z

        elif(self.collideWall(self.puck.x,self.puck.z)>0):
            self.bandera_movimiento=1
            self.movimiento=self.collideWall(self.puck.x,self.puck.z)
            self.difference_x=self.puck.x
            self.difference_z=self.puck.z-(-1.8)

        glutPostRedisplay()
        glutTimerFunc(5, self.onTimer, 1)

    def main(self):
        #Método principal del programa, se establecen todas las funciones.
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowPosition(200, 200)
        glutInitWindowSize(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        glutCreateWindow("Air Hockey 3D")
        self.glInit()
        self.gameInit()
        self.gameRestart()
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutSpecialFunc(self.keyInput)
        glutTimerFunc(5, self.onTimer, 1)
        glutKeyboardFunc(self.NormalkeyInput)
        glutMainLoop()
        return

#main=mesa()
#main.main()
app=QApplication(sys.argv)
win=mesa()
win.main()
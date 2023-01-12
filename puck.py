import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLE import *
from OpenGL.GLUT import * #Importada
import math

class Puck():
    """
    Clase para el Puck del juego
    """
    def __init__(self):
        """
        Constructor de la clase. Se colocan los atributos que contendrá el puck.
        """
        #Coordenadas y radio del puck
        self.x=0.0
        self.y=0.0
        self.z=0.0
        self.radius = self.height = 0.0
        self.r = self.g = self.b = 0.3
        self.dx=0
        #Variables para generar un circulo
        self.objCylinder = gluNewQuadric()
        self.objDisk = gluNewQuadric()
        self.mallets=[]
        self.walls=[]
        self.goals=[]
        self.SLICES_NUMBER = 20
        self.bandera=True
        self.STACKS_NUMBER = 10
        self.SPEED = 0.03
        self.EPS = 1e-6
        self.dz = -self.SPEED
        self.z=0

    def getX(self):
        #Método para obtener coordenada X
        return self.x

    def getY(self):
        #Método para obtener coordenada Y
        return self.y

    def getZ(self):
        #Método para obtener coordenada Z
        return self.z

    def getRadius(self):
        #Método para obtener el radio del Puck
        return self.radius
    
    def Puck2(self):
        if(self.objCylinder != None):
            gluDeleteQuadric(self.objCylinder)
        if (self.objDisk != None):
             gluDeleteQuadric(self.objDisk)

    def draw(self):
        """
        Método para dibujar el puck dentro de la mesa del juego.
        Colocando su color y dimensiones.
        """
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glColor3d(self.r, self.g, self.b)
        glTranslated(self.x, self.y, self.z)
        glNormal3d(0, 1, 0)
        glRotated(90, 1, 0, 0)
        gluCylinder(self.objCylinder, self.radius, self.radius, self.height, self.SLICES_NUMBER, self.STACKS_NUMBER);
        gluDisk(self.objDisk, 0.0, self.radius, self.SLICES_NUMBER, self.STACKS_NUMBER)
        glPopMatrix()

    def collide(self,x,z):
        equis=x
        zeta=z
        if(abs(equis-self.x)+abs(zeta-self.z)<0.505):
            return True
        else:
            return False

    def move(self,movimiento,dif_x,dif_z):
        """
        Método para establecer las direcciones del puck en caso de las colisiones 
        entre este y las paredes de la mesa.

        Args: dif_x y dif_z
        """
        #Frente
        if (dif_x>=0 and dif_x<0.1) and (dif_z>-0.25 and dif_z<=-0.18):
            self.z+=self.dz
            #print("llegue norte")
        #Noreste
        elif (dif_x>=0.1 and dif_x<0.2) and (dif_z>-0.18 and dif_z<=-0.1):
            self.z += self.dz  
            self.x -= self.dz
        #Este
        elif (dif_x>=0.2 and dif_x<0.3) and (dif_z>-0.1 and dif_z<=0.1):
            self.x -= self.dz
        #Sureste   
        elif (dif_x>=0.1 and dif_x<0.2) and (dif_z>0.1 and dif_z<0.3):
            self.x -= self.dz 
            self.z -= self.dz   
        #Sur
        elif (dif_x>=0 and dif_x<0.1) and (dif_z>=0.3 and dif_z<=0.2):
            self.z -= self.dz
        #Suroeste
        elif (dif_x>=-0.1 and dif_x<0) and (dif_z>0.1 and dif_z<0.3):
            self.x += self.dz 
            self.z -= self.dz 
        #Oeste
        elif (dif_x>-0.25 and dif_x<-0.1) and (dif_z>-0.1 and dif_z<=0.1):
            self.x += self.dz 
        #Noroeste
        elif (dif_x>=-0.1 and dif_x<0) and (dif_z>-0.2 and dif_z<=-0.1):
            self.x += self.dz 
            self.z += self.dz 
        else:
            #Condicionales para realizar movimientos del puck dependiendo del cuadrante de la mesa
            if (movimiento == True):
                self.z += self.dz 
            elif(movimiento==False):
                self.z -= self.dz 
            elif(movimiento==1):
                self.x -= self.dz 
                self.z -= self.dz 
            elif(movimiento==2):
                self.z -= self.dz 
            elif(movimiento==3):
                self.x += self.dz 
                self.z -= self.dz 
            elif(movimiento==4):
                self.x += self.dz 
            elif(movimiento==5):
                self.x += self.dz 
                self.z += self.dz 
            elif(movimiento==6):
                self.z += self.dz 
            elif(movimiento==7):
                self.x += self.dz 
                self.z -= self.dz 
            elif(movimiento==8):
                self.x -= self.dz 
            else:
                self.z-=self.dz
        return 

    def setPosition(self,ax,ay,az):
        """
        Método para establecer la posición del Puck dentro del juego

        Args: Coordenadas X,Y y Z
        """
        self.x = ax
        self.y = ay + self.height
        self.z = az
    def setParameter(self,aRadius,aHeight):
        """
        Método para establecer el radio del puck, así como su altura
        """
        self.radius = aRadius
        self.height = aHeight
    def setColor(self,a_r,a_g,a_b):
        #Método para establecer el color del puck
        self.r = a_r
        self.g = a_g
        self.b = a_b


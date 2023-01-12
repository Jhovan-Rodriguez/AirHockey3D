from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLE import *
from OpenGL.GLUT import * #Importada

class mallet():
    def __init__(self):
        """
        Constructor de la clase. Se colocan los atributos que contendrán los jugadores.
        """
        #Coordenadas y altura de cada jugador
        self.x=0.0
        self.y=0.0
        self.z=0.0
        self.height=0.0
        self.r = self.g = self.b = 0.3
        self.radius=0.0
        self.SLICES_NUMBER = 20
        self.STACKS_NUMBER = 10
        self.objCylinder = gluNewQuadric()
        self.objDisk = gluNewQuadric()
    
    def getX(self):
        #Método para obtener coordenada X
        return self.x
    def getZ(self):
        #Método para obtener coordenada Z
        return self.z
    def getRadius(self):
        #Método para obtener el radio de la ficha
        return self.radius

    def setColor(self,a_r,a_g,a_b):
        #Método para establecer el color de la ficha-jugador
        self.r = a_r
        self.g = a_g
        self.b = a_b

    def setParameter(self,aRadius,aHeight):
        """
        Método para establecer el radio de la ficha-jugador, así como su altura
        """
        self.radius = aRadius
        self.height = aHeight
    def setPosition(self,a_x,a_y,a_z):
        """
        Método para establecer la posición del jugador dentro del juego

        Args: Coordenadas X,Y y Z
        """
        self.x = a_x
        self.y = a_y + self.height
        self.z = a_z

    def draw(self):
        """
        Método para dibujar la ficha-jugador dentro de la mesa del juego.
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
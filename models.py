from pyglet.gl import *
from pyglet.window import key
import pyglet

import math

def draw_axis(axis_length, axis_origin):

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES) # X
    glVertex3f(*axis_origin)
    glVertex3f(axis_origin[0] + axis_length, axis_origin[1], axis_origin[2])
    glEnd()

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES) # Y
    glVertex3f(*axis_origin)
    glVertex3f(axis_origin[0], axis_origin[1] + axis_length, axis_origin[2])
    glEnd()

    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES) # Z
    glVertex3f(*axis_origin)
    glVertex3f(axis_origin[0], axis_origin[1], axis_origin[2] + axis_length)
    glEnd()

class Model3D:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.collision = False
        self.pos = [0, 0, 0]
        self.rot = [0, 0, 0]

    def enable_collision(self):
        set_collision = True

    def disable_collision(self):
        set_collision = False

    def draw(self):
        self.batch.draw()

class Light(Model3D):
    def __init__(self):
        super().__init__()
    
        color = ('c3f', (0,1,0)*4)

        self.especularidade  = (1.0, 1.0, 1.0, 1.0)
        self.especMaterial   = 40
        self.pos = [0.0, 5.0, 5.0]

        self.luzDifusa       = [1.0, 1.0, 1.0, 1.0]
        self.luzEspecular    = [1.0, 1.0, 1.0, 1.0]

        glMaterialfv(GL_FRONT, GL_SPECULAR, (GLfloat * 4)(*self.especularidade))
        glMateriali(GL_FRONT, GL_SHININESS, self.especMaterial)

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        x, y, z = self.pos
        X, Y, Z = x + 1, y + 1, z + 1

        self.batch.add(4, GL_QUADS, None, ('v3f',(X,y,z,x,y,z,x,Y,z,X,Y,z)), color)
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)), color)
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,y,z,x,y,Z,x,Y,Z,x,Y,z)), color)
        self.batch.add(4, GL_QUADS, None, ('v3f',(X,y,z,X,y,z,X,Y,z,X,Y,z)), color)

    def show(self):
        glLightfv(GL_LIGHT0, GL_DIFFUSE,  (GLfloat * 4)(*self.luzDifusa))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (GLfloat * 4)(*self.luzEspecular))
        glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat * 3)(*self.pos))
        self.draw()

class Cube(Model3D):
    def __init__(self):
        super().__init__()

        self.enable_collision()

        color = ('c3f', (1,1,1)*4)

        x, y, z = self.pos
        X, Y, Z = x + 1, y + 1, z + 1

        self.batch.add(4, GL_QUADS, None, ('v3f',(X,y,z,x,y,z,x,Y,z,X,Y,z)), color)
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)), color)
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,y,z,x,y,Z,x,Y,Z,x,Y,z)), color)
        self.batch.add(4, GL_QUADS, None, ('v3f',(X,y,z,X,y,z,X,Y,z,X,Y,z)), color)

class Ground(Model3D):
    def __init__(self):
        super().__init__()

        self.enable_collision()

        color = ('c3f', (0, 1, 1)*4)

        self.batch.add(4, GL_QUADS, None, ('v3f', (100, 0, 0, -100, 0, 0, 0, 0, 100, -100, 0, -100)))

class Camera():
    def __init__(self):
        self.pos = [0, 0, 0]
        self.rot = [0, 0]

    def mouse_motion(self, dx, dy):
        dx /= 10
        dy /= 10

        self.rot[0] += dy
        self.rot[1] -= dx

        if self.rot[0] > 90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90

    def move(self):
        glRotatef(-self.rot[0], 1, 0, 0)
        glRotatef(-self.rot[1], 0, 1, 0)
        x, y, z = self.pos
        glTranslatef(-x, -y, -z)

    def update(self, dt, keys):
        s = dt * 10
        rotY = -self.rot[1]/180*math.pi
        dx, dz = s*math.sin(rotY), s*math.cos(rotY)
        if keys[key.W]:
            self.pos[0] += dx
            self.pos[2] -= dz
        if keys[key.S]:
            self.pos[0] -= dx
            self.pos[2] += dz
        if keys[key.A]:
            self.pos[0] -= dz
            self.pos[2] -= dx
        if keys[key.D]:
            self.pos[0] += dz
            self.pos[2] += dx

        if keys[key.SPACE]:
            self.pos[1] += s
        if keys[key.LSHIFT]:
            self.pos[1] -= s
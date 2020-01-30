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
        self.batch     = pyglet.graphics.Batch()
        self.collision = False
        self.gravity   = False
        self.pos       = [0.0, 0.0, 0.0]
        self.rot       = [0.0, 0.0, 0.0]
        self.rotvel    = [0.0, 0.0, 0.0]
        self.yvel      = [0.0, 0.0, 0.0]
        self.yaccel    = [0.0, -9.8, 0.0]
        self.hvel      = [0.0, 0.0, 0.0]
        self.haccel    = [0.0, 0.0, 0.0]
        self.force     = [0.0, 0.0, 0.0]
        self.lmomentum = [0.0, 0.0, 0.0]
        self.wmomentum = [0.0, 0.0, 0.0]
        self.friction  = 1.01

    def enable_collision(self):
        self.collision = True

    def disable_collision(self):
        self.collision = False
    
    def enable_gravity(self):
        self.gravity = True

    def disable_gravity(self):
        self.gravity = False
    
    def update(self, dt, keys):
        if self.gravity:
            self.yvel[0] += self.yaccel[0] * dt
            self.yvel[1] += self.yaccel[1] * dt
            self.yvel[2] += self.yaccel[2] * dt

            self.pos[0] += self.yvel[0] * dt
            self.pos[1] += self.yvel[1] * dt
            self.pos[2] += self.yvel[2] * dt

        self.hvel[0] += self.haccel[0] * dt
        self.hvel[1] += self.haccel[1] * dt
        self.hvel[2] += self.haccel[2] * dt

        self.hvel[0] /= self.friction
        self.hvel[1] /= self.friction
        self.hvel[2] /= self.friction

        self.pos[0] += self.hvel[0] * dt
        self.pos[1] += self.hvel[1] * dt
        self.pos[2] += self.hvel[2] * dt

        self.rotvel[0] /= self.friction
        self.rotvel[1] /= self.friction

        self.rot[0] += self.rotvel[0] * dt
        self.rot[1] += self.rotvel[1] * dt

    def draw(self):
        glPushMatrix()
        x, y, z = self.pos
        glRotatef(self.rot[0], 1, 0, 0)
        glRotatef(self.rot[1], 0, 1, 0)
        glTranslatef(x, y, z)
        self.batch.draw()
        glPopMatrix()

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
        X, Y, Z = x + .1, y + .1, z + .1

        self.batch.add(4, GL_QUADS, None, ('v3f',(X,y,z,x,y,z,x,Y,z,X,Y,z)), color) # frente
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)), color) # tras
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,y,z,x,y,Z,x,Y,Z,x,Y,z)), color) # esquerda
        self.batch.add(4, GL_QUADS, None, ('v3f',(X,y,z,X,y,Z,X,Y,Z,X,Y,z)), color) # direita
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,Y,z,x,Y,Z,X,Y,Z,X,Y,z)), color) # cima
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,y,z,x,y,Z,X,y,Z,X,y,z)), color) # baixo

    def show(self):
        glLightfv(GL_LIGHT0, GL_DIFFUSE,  (GLfloat * 4)(*self.luzDifusa))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (GLfloat * 4)(*self.luzEspecular))
        glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat * 3)(*self.pos))
        self.draw()
class Cube(Model3D):
    def __init__(self, size, position, color):
        super().__init__()

        self.enable_collision()
        self.enable_gravity()

        self.size = size

        x, y, z = self.pos
        X, Y, Z = x + size, y + size, z + size

        self.batch.add(4, GL_QUADS, None, ('v3f',(X,y,z,x,y,z,x,Y,z,X,Y,z)), color) # frente
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)), color) # tras
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,y,z,x,y,Z,x,Y,Z,x,Y,z)), color) # esquerda
        self.batch.add(4, GL_QUADS, None, ('v3f',(X,y,z,X,y,Z,X,Y,Z,X,Y,z)), color) # direita
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,Y,z,x,Y,Z,X,Y,Z,X,Y,z)), color) # cima
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,y,z,x,y,Z,X,y,Z,X,y,z)), color) # baixo

        self.pos = position

class Ground(Model3D):
    def __init__(self):
        super().__init__()

        self.enable_collision()

        color = ('c3f', (0, 0.4, 0)*4)

        x, y, z = self.pos
        X, Y, Z = x + 100, y + 100, z + 100

        self.batch.add(4, GL_QUADS, None, ('v3f', (-X, y, Z, -X, y, -Z, X, y, -Z, X, y, Z)), color)

class Camera():
    def __init__(self):
        self.pos = [0, 5, 30]
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
        glTranslatef(-self.pos[0], -self.pos[1], -self.pos[2])

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
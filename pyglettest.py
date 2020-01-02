from pyglet.gl import *
from pyglet.window import key
import pyglet

import math

class Model:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        color = ('c3f', (1,1,1)*4)

        x, y, z = 0, 0, -1
        X, Y, Z = x + 1, y + 1, z + 1

        self.batch.add(4, GL_QUADS, None, ('v3f',(X,y,z,x,y,z,x,Y,z,X,Y,z)), color)
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)), color)
        self.batch.add(4, GL_QUADS, None, ('v3f',(x,y,z,x,y,Z,x,Y,Z,x,Y,z)), color)
        self.batch.add(4, GL_QUADS, None, ('v3f',(X,y,z,X,y,z,X,Y,z,X,Y,z)), color)

    def draw(self):
        self.batch.draw()

def draw_axis():
    axis_length = 1000

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES) # X
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(axis_length, 0.0, 0.0)
    glEnd()

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES) # Y
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, axis_length, 0.0)
    glEnd()

    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES) # Z
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, axis_length)
    glEnd()

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

class Window(pyglet.window.Window):

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self: self.lock, setLock)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300, 200)

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        pyglet.clock.schedule(self.update)

        self.model = Model()
        self.camera = Camera()

    def projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def modelview(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set3d(self):
        self.projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.modelview()
    
    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock:
            self.camera.mouse_motion(dx, dy)

    def on_key_press(self, KEY, MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.Q:
            self.mouse_lock = not self.mouse_lock
    
    def update(self, dt):
        self.camera.update(dt, self.keys)

    def on_draw(self):
        self.clear()
        draw_axis()
        self.set3d()
        rot = self.camera.rot
        glRotatef(-rot[0], 1, 0, 0)
        glRotatef(-rot[1], 0, 1, 0)
        x, y, z = self.camera.pos
        glTranslatef(-x, -y, -z)
        self.model.draw()

if __name__ == "__main__":
    w, h = 800, 480
    windows = Window(width=w, height=h, caption="Test", resizable=True)
    glClearColor(0.5, 0.5, 0.5, 1)
    pyglet.app.run()
from pyglet.gl import *
from pyglet.window import key
import pyglet

from models import Light, Cube, Camera, Ground, draw_axis
from utils import collision, ground_collision
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

        self.gl_init()

        pyglet.clock.schedule(self.update)

        self.models = []

        # self.add_models(Cube(1, [0,10,0], ('c3f', (1,1,1)*4)))
        # self.add_models(Cube(2, [2,20,0], ('c3f', (0,1,1)*4)))
        # self.add_models(Cube(2, [1,40,1], ('c3f', (1,1,0)*4)))

        self.add_models(Cube(2, [0, 0, 0], ('c3f', (1,1,0)*4)))
        self.add_models(Cube(2, [0, 0, 10], ('c3f', (1,1,1)*4)))

        self.models[0].haccel = [0.0, 0.0, 1.0]
        self.models[1].haccel = [0.0, 0.0, -1.0]

        self.add_models(Cube(2, [10, 0, 0], ('c3f', (1,1,0)*4)))
        self.add_models(Cube(2, [20, 0, 0], ('c3f', (1,1,1)*4)))

        self.models[2].haccel = [1.0, 0.0, 0.0]
        self.models[3].haccel = [-1.0, 0.0, 0.0]

        self.camera = Camera()
        self.ground = Ground()
        self.light = Light()

    def add_models(self, model):
        self.models.append(model)

    def gl_init(self):
        glClearColor(0.5, 0.5, 0.5, 1)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)

    def projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def modelview(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set3d(self):
        self.projection()
        gluPerspective(90, self.width/self.height, 0.05, 1000)
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

        for model in self.models:
            model.update(dt, self.keys)

    def on_draw(self):
        self.clear()
        draw_axis(3, (-1, 1, -1))
        self.set3d()
        self.camera.move()
        self.light.show()
        self.ground.draw()

        for i in range(len(self.models)):
            for j in range(len(self.models)):
                if i != j:
                    collision(self.models[i], self.models[j])
            
            ground_collision(self.models[i], self.ground)

        for model in self.models:
            model.draw()

if __name__ == "__main__":
    w, h = 800, 600
    windows = Window(width=w, height=h, caption="Test", resizable=True)
    pyglet.app.run()
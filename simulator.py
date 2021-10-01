
import pyglet
from pyglet.window import mouse, key
import yaml
import numpy as np
from math import cos, sin, pi, sqrt, exp, fabs

class Robot():

    def __init__(self):

        posx = 0.0
        posy = 0.0
        self.pos = pos = np.hstack((posx, posy))
        self.angle = np.random.uniform(0.0, 2.0*pi)

        self.body_radius = 0.15

        self.batch = pyglet.graphics.Batch()

        circle = self.body_radius*np.vstack([[cos(phi), sin(phi)] for phi in np.linspace(0., 2.*pi, 20)])
        triangle = 0.5*self.body_radius*np.vstack([[cos(phi)+0.6, sin(phi)] for phi in np.linspace(0., 2.*pi, 4)])
        trajectory = np.vstack([[x, sin(x*3)] for x in np.linspace(0., 2., 20)])

        g1 = pyglet.graphics.Group()
        g2 = pyglet.graphics.Group()
        g3 = pyglet.graphics.Group()

        self.batch.add(len(circle), pyglet.gl.GL_LINE_STRIP, g1,
            ('v2f', circle.flatten()),
        )

        self.batch.add(len(triangle), pyglet.gl.GL_LINE_STRIP, g2,
            ('v2f', triangle.flatten()),
        )

        self.batch.add(len(trajectory), pyglet.gl.GL_LINE_STRIP, g3,
            ('v2f', trajectory.flatten()),
        )

    def draw(self):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(self.pos[0], self.pos[1], 0)
        pyglet.gl.glRotatef(180./pi*self.angle, 0, 0, 1)
        self.batch.draw()
        pyglet.gl.glPopMatrix()

    def pred(self, linear, angular):
        #traj[0] = pos/ang
        #for i in 
        pass

    def move(self, linear, angular):
        self.pos += np.array([cos(self.angle), sin(self.angle)])*linear
        self.angle += angular

def main():

    robot = Robot()
    keys = key.KeyStateHandler()

    def update(dt):
        max_lin = 0.2*3
        max_ang = 1.0*3
        linear = 0.0
        angular = 0.0
        if keys[key.UP] or keys[key.W]:
            linear += max_lin
        if keys[key.DOWN] or keys[key.S]:
            linear -= max_lin
        if keys[key.LEFT] or keys[key.A]:
            angular += max_ang
        if keys[key.RIGHT] or keys[key.D]:
            angular -= max_ang
    
        linear *= dt
        angular *= dt

        robot.pred(linear, angular)

        #robot.move(linear, angular)

    window_width = 600
    window_height = 600
    window = pyglet.window.Window(window_width, window_height)
    
    # Window handlers
    window.push_handlers(keys)

    # Update every 60 times per second
    pyglet.clock.schedule_interval(update, 1 / 60.0)

    # Map
    env = pyglet.image.load('env.png')
    env.anchor_x = env.width // 2
    env.anchor_y = env.height // 2

    batch = pyglet.graphics.Batch()

    PX_TO_METER = 10.0

    @window.event
    def on_draw():

        window.clear()
        
        pyglet.gl.glPushMatrix()
        pyglet.gl.glRotatef(90, 0, 0, 1)
        pyglet.gl.glTranslatef(window_height/2, -window_width/2, 0)
        pyglet.gl.glScalef(55, 55, 1)

        pyglet.gl.glPushMatrix()
        pyglet.gl.glRotatef(-90, 0, 0, 1)
        pyglet.gl.glScalef(1.0/PX_TO_METER, 1.0/PX_TO_METER, 1)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST) 
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
        env.blit(0, 0, 0)
        pyglet.gl.glPopMatrix()

        robot.draw()

        pyglet.gl.glPopMatrix()

    pyglet.app.run()

if __name__ == "__main__":
    main()

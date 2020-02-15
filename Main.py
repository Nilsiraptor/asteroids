import pyglet
import math
import random as rng

window = pyglet.window.Window(800, 600)
window.set_caption("Game")

@window.event
def on_draw():
    window.clear()

@window.event
def on_key_press(symbol, modifier):
    pass

pyglet.app.run()

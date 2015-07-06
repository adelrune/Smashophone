import pygame
from pyo import *
from jsynth import *
s = Server().boot()
pygame.init()
ssb = SimpleSynthBlam()

ssb.out()

s.start()
s.setAmp(0.3)
s.gui(locals)


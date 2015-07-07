import pygame
from pyo import *
from jsynth import *
#Starts pyo and pygame
s = Server().boot()
pygame.init()
#Creates the synth and call its out method
ssb = ExampleSynth()
ssb.out()

#starts the pyo server and calls the gui.
s.start()
s.setAmp(0.3)
s.gui(locals)


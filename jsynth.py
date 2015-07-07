from __future__ import division
import pygame
from pyo import *

gc_mayflash_2_ports = {"a":(1,"d"), "b":(2,"d"), "x":(0,"d"),
    "y":(3,"d"), "start":(9,"d"), "l_digital":(4,"d"),
    "r_digital":(5,"d"),"dpad_u":(12,"d"), "dpad_d":(14,"d"), 
    "dpad_l":(15,"d"), "dpad_r":(13,"d"), "left_stick_y":(1,"a"), 
    "left_stick_x":(0,"a"), "right_stick_y":(2,"a"),
    "right_stick_x":(5,"a"), "l_analog":(3,"a"),"r_analog":(4,"a"),
    "z":(7,"d")
}

class JSynth:
    """This is a basic class that defines a metronome calling a value fetching fuction
60 times a second. The button values are fetched from the controller mapping argument
which should be a dictionnary with input names as keys and a tuple containing the 
sdl maping of the input as the first element and a string equal to "a" if the input
is analogue, "d" if the input is digital or "b" if the input is a trackball.
The basic values generated from the inputs are pyo Sigs which
can be passed to any pyo object and will update in real time.
Each button name in the values dictionary
also have a pyo trigger output at name+"_t". """
    def __init__(self,controller_mapping, joynb=0):
        #Mayflash 2 port gamecube->usb adapter to sdl input mapping. d means digital
        #and a means analog. This is the thing you have to change
        self._joystick = pygame.joystick.Joystick(joynb)
        self._joystick.init()
        self.button_mappings = controller_mapping
        self.values = {}
        for k in self.button_mappings:
            if self.button_mappings[k][1] == "d":
                self.values[k] = Sig(0)
            else:
                self.values[k] = SigTo(0)
            self.values[k+"_t"] = Thresh(self.values[k], threshold=0.8)
        self.metronome = Metro(1/60).play()
        self.t_f = TrigFunc(self.metronome, self.update)

    def update(self):
        functions = {"d":self._joystick.get_button,
        "a":self._joystick.get_axis, "b":self._joystick.get_ball}
        pygame.event.pump()
        for k in self.button_mappings:
            vals = self.button_mappings[k]
            self.values[k].setValue(functions[vals[1]](vals[0]))

    def out(self):
        self.stream = self.last_audio_object.out()

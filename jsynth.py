from __future__ import division
import pygame
from pyo import *

class JSynth:
    """This is a basic class that defines a metronome calling a value fetching fuction
60 times a second. The basic values included in this class are pyo Sigs which
can be passed to any pyo object and will update in real time.

The values specified in this class assumes a gamecube controller with a 
mayflash two port adapter, the names and the amount of actual inputs may be
different with different controllers, adapt this class to them if other models
of controller/adapters are used."""
    def __init__(self,joynb=0):
        #Mayflash 2 port gamecube->usb adapter to sdl input mapping. d means digital
        #and a means analog. This is the thing you have to change
        self._joystick = pygame.joystick.Joystick(joynb)
        self._joystick.init()
        self.button_mappings = {"a":(1,"d"), "b":(2,"d"), "x":(0,"d"),
            "y":(3,"d"), "start":(9,"d"), "l_digital":(4,"d"),
            "r_digital":(5,"d"),"dpad_u":(12,"d"), "dpad_d":(14,"d"), 
            "dpad_l":(15,"d"), "dpad_r":(13,"d"), "left_stick_y":(1,"a"), 
            "left_stick_x":(0,"a"), "right_stick_y":(2,"a"),
            "right_stick_x":(5,"a"), "l_analog":(3,"a"),"r_analog":(4,"a"),
            "z":(7,"d")
        }
        self.values = {}
        for k in self.button_mappings:
            self.values[k] = Sig(0)
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


class SimpleSynthBlam(JSynth):
    def __init__(self,joynb=0):
        JSynth.__init__(self)
        self.osc = LFO(freq=500+(self.values["l_analog"]+self.values["r_analog"]-1)*250)
        self.snd = SndTable(["tlick.wav","pouc.wav","ptoui.wav","tchou.wav"])
        self.trigger = Thresh([self.values["a"],self.values["b"],self.values["x"],self.values["y"]],threshold=0.9)
        self.reader = TrigEnv(self.trigger, table=self.snd, dur=self.snd.getDur()).out()
        self.filtr = Biquad(self.osc, freq=700+self.values["left_stick_x"]*600, q=20+self.values["left_stick_y"]*19, mul=0.2)
        self.last_audio_object = self.filtr
        

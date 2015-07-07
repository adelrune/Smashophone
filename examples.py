import jsynth
from pyo import *
from __future__ import division

class ExampleSynth(jsynth.JSynth):
    def __init__(self,joynb=0):
        jsynth.JSynth.__init__(self, jsynth.gc_mayflash_2_ports, joynb)
        self.osc_beat = Metro(time=[1/2, 1/3]).play()
        self.osc_envelope = TrigExpseg(self.osc_beat, list=[(0,0),(0.06,1),(0.3,0)], exp=3)
        self.osc = LFO(freq=[700+(self.values["r_analog"])*430,
            300+(self.values["l_analog"])*130
            ], sharp=self.values["left_stick_y"], mul=self.osc_envelope
        )
        self.snd = SndTable(["snds/tlick.wav","snds/pouc.wav","snds/ptoui.wav","snds/tchou.wav"])
        self.reader = TrigEnv([self.values["a_t"],self.values["b_t"],self.values["x_t"],self.values["y_t"]],
            table=self.snd, dur=self.snd.getDur(), mul=0.8)
        self.filtr = Biquad(self.osc, freq=1000+self.values["left_stick_x"]*800, q=20+self.values["left_stick_y"]*19, mul=0.2)
        #important or the out method wont work.
        self.last_audio_object = Pan((self.reader+self.filtr).mix())


class ZeroGravitySynth(jsynth.JSynth):
    def __init__(self, joynb=0):
        jsynth.JSynth.__init__(self,jsynth.gc_mayflash_2_ports, joynb)

        # Sound on missiles
        self.sb_snd = SndTable("snds/coq.wav")
        self.sb_trig = Trig()
        self.sb_trigfunc = TrigFunc(self.values["b_t"], self.sb_play)
        self.sb_reader = TrigEnv(self.sb_trig, table=self.sb_snd, dur=self.sb_snd.getDur())

        # Sound on bomb
        self.db_snd = SndTable("snds/tssst.wav")
        self.db_trig = Trig()
        self.db_trigfunc = TrigFunc(self.values["b_t"], self.db_play)
        self.db_reader = TrigEnv(self.db_trig, table=self.db_snd, dur=self.db_snd.getDur())

        # Sound on jump
        self.j_snd = SndTable("snds/iiiii.wav")
        self.j_trigger = Thresh(self.values["x"] + self.values["y"], threshold=0.9)
        self.j_reader = TrigEnv(self.j_trigger, table=self.j_snd, dur=self.j_snd.getDur())

        # Base oscillator
        self.osc = LFO(freq=440 - self.values["l_analog"] * 100 + self.values["left_stick_x"] * 30, mul=0.2)

        self.lfo = Biquad(self.osc, freq=1500-(self.values["l_analog"]) * 1500)

        self.pan = Pan((self.sb_reader + self.db_reader + self.j_reader + self.lfo).mix(0))

        self.last_audio_object = self.pan

    def sb_play(self):
        if abs(self.values["left_stick_x"].value) > 0.7:
            self.sb_trig.play()

    def db_play(self):
        if self.values["left_stick_y"].value > 0.7:
            self.db_trig.play()

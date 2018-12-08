# Smashophone
*Template to create joystick controlled synthetisers using pyo and pygame*

The jsynth module takes advantage of the combined capabilities of pyo and pygame to enable the use of a game controller to send events and control continuous parameters of any kind of pyo objects.

The JSynth class is designed to make it possible to use any kind of controller recognized by pygame (even though the only controler supported as of now is the mayflash 2 ports gamecube controller adapter).

The different analog and digital inputs are polled 60 times a second and the variations of the analog values are smoothed by pyo's SigTo object. The class also sends a trigger for every analog inpu that crosses 80% of its value.

The examples provided with the code are very simple use cases of the JSynth class used to demonstrate the trigger fonctionalities and the continuous parameters.
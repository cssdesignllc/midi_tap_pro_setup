# midi_tap_pro_setup
MIDI Tap Pro Setup Utility - This utility is used to configure a MIDI Tap Pro MIDI Interface.<br>
Refer to the MIDI Tap Pro user manual for specifics on communication.<br>
Use this utility as is or modify it for a custom experience.
## Dependencies
* [Python](https://www.python.org/)
* [mido](https://pypi.org/project/mido/)
* [python-rtmidi](https://pypi.org/project/python-rtmidi/)
## Setup
There are many ways to run a python program, this is just another...
1. Clone this project
2. Open terminal and navigate to this project
3. Create virtual environment (Windows example below)
```console
py -m venv .venv
.venv\Scripts\activate
pip install mido
pip install python-midi
```
4. Run the program
```console
py main.py
```
## Usage
![app](https://github.com/cssdesignllc/midi_tap_pro_setup/blob/main/image/mtp_main.jpg)
1. The app should find the MIDI Tap Pro automatically and assign the correct in and out ports, if not, find the highest numbered ports with 'MIDI Tap Pro' in the name. The highest numbered ports are the virtual ports which is used for configuration.
2. Press the 'Open MIDI' button to open the in and out ports.
3. MIDI Tap Setup Tab - basic configuration, see user manual for specifics.
4. MIDI Tap Stats - gather statistics.
5. MIDI Tap Display - example drawing (note, display must be first set to 'custom').
6. MIDI Tap Update - update the MIDI Tap firmware using an update file provided by CSS Designs (found on our website https://cssdesignllc.com).
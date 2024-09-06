# MIT License
#
# Copyright (c) 2024 CSS Designs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import mido
from tabs.tab_base import TabBase
from tkinter import ttk
from midi.midi_port_comm import MidiPortComm
from frames.frame_midi_tap_stats import FrameMidiTapStats


class TabMidiTapStats(TabBase):
    def __init__(self, master: ttk.Notebook, comm_manager: MidiPortComm):
        super().__init__(master, "MIDI Tap Stats", comm_manager)

        self.frame_midi_tap_stats = FrameMidiTapStats(self, comm_manager)
        self.frame_midi_tap_stats.grid(column=0, row=0, padx=5, pady=5, sticky='n')

    def rx_handler(self, message: mido.Message):
        self.frame_midi_tap_stats.rx_handler(message)
        pass

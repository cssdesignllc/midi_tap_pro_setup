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
from frames.frame_base import FrameBase
from midi.midi_port_comm import MidiPortComm
from tkinter.ttk import *
from midi.midi_tap_commands import MidiTapCommands


class FrameMidiTapStats(FrameBase):
    def __init__(self, parent, comm_manager: MidiPortComm):
        super().__init__(parent, comm_manager)

        self.parent = parent

        self.grid_columnconfigure(7, weight=1)

        row = 0

        # GET STATS
        Button(self, text="Get Stats", width=15, command=self.get_stats).grid(column=0, row=row, sticky='nw', padx=5, pady=5)
        columns = ('stat', 'bytes', 'errors', 'overruns')
        self.stats_treeview = Treeview(self, columns=columns, show='headings', height=20)
        self.stats_treeview.heading('stat', text='Stat')
        self.stats_treeview.heading('bytes', text='Total Bytes')
        self.stats_treeview.heading('errors', text='Total Errors')
        self.stats_treeview.heading('overruns', text='Total Buffer Overruns')
        self.stats_treeview.grid(column=1, row=row, sticky='w', padx=5, pady=5, columnspan=6, rowspan=15)

        # RESET STATS
        row += 1
        Button(self, text="Reset Stats", width=15, command=self.reset_stats).grid(column=0, row=row, sticky='nw', padx=5, pady=5)

    def reset_stats(self):
        message = MidiTapCommands.build_reset_stats_command()
        self.comm_manager.write(mido.Message.from_bytes(message))

    def get_stats(self):
        message = MidiTapCommands.build_get_stats_command()
        self.comm_manager.write(mido.Message.from_bytes(message))

    def stats_payload_to_int(self, payload, offset):
        value = 0
        value |= (payload[offset + 0] << 0 ) & 0x0000000F
        value |= (payload[offset + 1] << 4 ) & 0x000000F0
        value |= (payload[offset + 2] << 8 ) & 0x00000F00
        value |= (payload[offset + 3] << 12) & 0x0000F000
        value |= (payload[offset + 4] << 16) & 0x000F0000
        value |= (payload[offset + 5] << 20) & 0x00F00000
        value |= (payload[offset + 6] << 24) & 0x0F000000
        value |= (payload[offset + 7] << 28) & 0xF0000000
        return value

    def stats_payload_to_short(self, payload, offset):
        value = 0
        value |= (payload[offset + 0] << 0 ) & 0x0000000F
        value |= (payload[offset + 1] << 4 ) & 0x000000F0
        value |= (payload[offset + 2] << 8 ) & 0x00000F00
        value |= (payload[offset + 3] << 12) & 0x0000F000
        return value

    def stats_rx(self, message: mido.Message):

        packet = message.bytes()
        if len(packet) < 5:
            return

        names = ("MIDI UART 1 IN", "MIDI UART 1 OUT", "MIDI USB 1 IN", "MIDI USB 1 OUT",
                 "MIDI UART 2 IN", "MIDI UART 2 OUT", "MIDI USB 2 IN", "MIDI USB 2 OUT",
                 "MIDI UART 3 IN", "MIDI UART 3 OUT", "MIDI USB 3 IN", "MIDI USB 3 OUT",
                 "USB UART IN", "USB UART OUT")

        # clear all rows
        for row in self.stats_treeview.get_children():
            self.stats_treeview.delete(row)

        index = 6
        for i in range(14):

            self.stats_treeview.insert('', i, values=(names[i],
                                                      str(self.stats_payload_to_int(packet, index)),
                                                      str(self.stats_payload_to_short(packet, index + 8)),
                                                      str(self.stats_payload_to_short(packet, index + 12))))
            index += 16

    def rx_handler(self, message: mido.Message):
        if message.type == 'sysex':
            if MidiTapCommands.get_command_type(message.bytes()) == MidiTapCommands.COMMAND_GET_STATS:
                self.stats_rx(message)

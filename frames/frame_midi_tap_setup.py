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

from tkinter import messagebox
import mido
from frames.frame_base import FrameBase
from midi.midi_port_comm import MidiPortComm
import tkinter as tk
from tkinter.ttk import *
from midi.midi_tap_commands import MidiTapCommands
from midi.midi_tap_commands import MidiTapResults


class FrameMidiTapSetup(FrameBase):
    def __init__(self, parent, comm_manager: MidiPortComm):
        super().__init__(parent, comm_manager)

        self.parent = parent

        self.grid_columnconfigure(7, weight=1)

        row = 0

        # SET MIDI THRU
        self.midi_thru_state = tk.BooleanVar()
        self.midi_thru_port = tk.IntVar(value=0)
        Button(self, text="Set MIDI Thru", width=15, command=self.set_midi_thru).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Checkbutton(self, text="enable", variable=self.midi_thru_state, onvalue=True, offvalue=False).grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Radiobutton(self, text="port 1", variable=self.midi_thru_port, value=0).grid(column=2, row=row, sticky='w', padx=5, pady=5)
        Radiobutton(self, text="port 2", variable=self.midi_thru_port, value=1).grid(column=3, row=row, sticky='w', padx=5, pady=5)
        Radiobutton(self, text="port 3", variable=self.midi_thru_port, value=2).grid(column=4, row=row, sticky='w', padx=5, pady=5)

        # SEPARATOR
        row = row + 1
        Separator(self, orient='horizontal').grid(
            row=row, columnspan=8, sticky="we"
        )

        # SET MIDI UART PORT
        row += 1
        self.uart_port = tk.IntVar(value=0)
        Button(self, text="Set UART Port", width=15, command=self.set_uart_port).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Radiobutton(self, text="port 1", variable=self.uart_port, value=0).grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Radiobutton(self, text="port 2", variable=self.uart_port, value=1).grid(column=2, row=row, sticky='w', padx=5, pady=5)
        Radiobutton(self, text="port 3", variable=self.uart_port, value=2).grid(column=3, row=row, sticky='w', padx=5, pady=5)

        # SEPARATOR
        row = row + 1
        Separator(self, orient='horizontal').grid(
            row=row, columnspan=8, sticky="we"
        )

        # SET BACKLIGHT
        row += 1
        self.backlight_level = tk.IntVar(value=50)
        Button(self, text="Set Backlight", width=15, command=self.set_backlight).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Level (10-100)").grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.backlight_level).grid(column=2, row=row, sticky='w', padx=5, pady=5)

        # SEPARATOR
        row = row + 1
        Separator(self, orient='horizontal').grid(
            row=row, columnspan=8, sticky="we"
        )

        display_items = [
            "three port icon",
            "single port stats",
            "single port bandwidth",
            "single port activity bars",
            "three port in activity bars",
            "three port out activity bars",
            "three port activity bars",
            "single port in activity raw",
            "single port out activity raw",
            "single port activity raw",
            "custom",
            "single port in midi events",
            "single port out midi events",
        ]

        # SET DISPLAY
        row += 1
        self.display = tk.StringVar(value=display_items[0])
        self.display_port = tk.IntVar(value=0)
        Button(self, text="Set Display", width=15, command=self.set_display).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        self.combobox_display = Combobox(self, values=display_items, textvariable=self.display, width=30, state="readonly")
        self.combobox_display.grid(column=1, row=row, sticky='w', padx=5, pady=5, columnspan=3)
        row += 1
        Label(self, text="single port selection").grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Radiobutton(self, text="port 1", variable=self.display_port, value=0).grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Radiobutton(self, text="port 2", variable=self.display_port, value=1).grid(column=2, row=row, sticky='w', padx=5, pady=5)
        Radiobutton(self, text="port 3", variable=self.display_port, value=2).grid(column=3, row=row, sticky='w', padx=5, pady=5)

        # SEPARATOR
        row = row + 1
        Separator(self, orient='horizontal').grid(
            row=row, columnspan=8, sticky="we"
        )

        # SAVE SETTINGS
        row += 1
        Button(self, text="Save Settings", width=15, command=self.save_settings).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="<-- save only required to persist settings between power cycles").grid(column=1, row=row, sticky='w', padx=5, pady=5, columnspan=4)

        # SEPARATOR
        row = row + 1
        Separator(self, orient='horizontal').grid(
            row=row, columnspan=8, sticky="we"
        )

        # FACTORY DEFAULTS
        row += 1
        Button(self, text="Factory Defaults", width=15, command=self.factory_defaults).grid(column=0, row=row, sticky='w', padx=5, pady=5)

        # SEPARATOR
        row = row + 1
        Separator(self, orient='horizontal').grid(
            row=row, columnspan=8, sticky="we"
        )

        # PAUSE/RESUME DISPLAY
        row += 1
        Button(self, text="Pause Display", width=15, command=self.pause_display).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Button(self, text="Resume Display", width=15, command=self.resume_display).grid(column=1, row=row, sticky='w', padx=5, pady=5)

    def set_midi_thru(self):
        message = MidiTapCommands.build_set_thru_command(self.midi_thru_port.get(), self.midi_thru_state.get())
        self.comm_manager.write(mido.Message.from_bytes(message))

    def set_backlight(self):
        if self.backlight_level.get() < 10 or self.backlight_level.get() > 100:
            messagebox.showerror("error", "invalid backlight value")
            return
        message = MidiTapCommands.build_set_backlight_command(self.backlight_level.get())
        self.comm_manager.write(mido.Message.from_bytes(message))

    def set_uart_port(self):
        message = MidiTapCommands.build_set_uart_port_command(self.uart_port.get())
        self.comm_manager.write(mido.Message.from_bytes(message))

    def set_display(self):
        message = MidiTapCommands.build_set_screen_command(self.combobox_display.current() + 1, self.display_port.get())
        self.comm_manager.write(mido.Message.from_bytes(message))

    def save_settings(self):
        message = MidiTapCommands.build_save_settings_command()
        self.comm_manager.write(mido.Message.from_bytes(message))

    def factory_defaults(self):
        if messagebox.askokcancel("confirm", "are you sure you want to set factory defaults?"):
            message = MidiTapCommands.build_factory_defaults_command()
            self.comm_manager.write(mido.Message.from_bytes(message))

    def pause_display(self):
        message = MidiTapCommands.build_pause_display_command(True)
        self.comm_manager.write(mido.Message.from_bytes(message))

    def resume_display(self):
        message = MidiTapCommands.build_pause_display_command(False)
        self.comm_manager.write(mido.Message.from_bytes(message))

    def rx_handler(self, message: mido.Message):
        if message.type == 'sysex':
            packet = message.bytes()
            if MidiTapCommands.get_command_type(packet) == MidiTapCommands.COMMAND_SET_THRU:
                if packet[5] != MidiTapResults.RESULT_SUCCESS.value:
                    messagebox.showerror("midi tap pro", "failed to set thru! error " + str(packet[5]))
            elif MidiTapCommands.get_command_type(packet) == MidiTapCommands.COMMAND_SET_UART:
                if packet[5] != MidiTapResults.RESULT_SUCCESS.value:
                    messagebox.showerror("midi tap pro", "failed to set uart port! error " + str(packet[5]))
            elif MidiTapCommands.get_command_type(packet) == MidiTapCommands.COMMAND_SET_BACKLIGHT:
                if packet[5] != MidiTapResults.RESULT_SUCCESS.value:
                    messagebox.showerror("midi tap pro", "failed to set backlight! error " + str(packet[5]))
            elif MidiTapCommands.get_command_type(packet) == MidiTapCommands.COMMAND_SET_SCREEN:
                if packet[5] != MidiTapResults.RESULT_SUCCESS.value:
                    messagebox.showerror("midi tap pro", "failed to set screen! error " + str(packet[5]))
            elif MidiTapCommands.get_command_type(packet) == MidiTapCommands.COMMAND_SAVE_SETTINGS:
                if packet[5] != MidiTapResults.RESULT_SUCCESS.value:
                    messagebox.showerror("midi tap pro", "failed to save settings! error " + str(packet[5]))
            elif MidiTapCommands.get_command_type(packet) == MidiTapCommands.COMMAND_FACTORY_DEFAULTS:
                if packet[5] != MidiTapResults.RESULT_SUCCESS.value:
                    messagebox.showerror("midi tap pro", "failed to set factory defaults! error " + str(packet[5]))
            elif MidiTapCommands.get_command_type(packet) == MidiTapCommands.COMMAND_PAUSE_DISPLAY:
                if packet[5] != MidiTapResults.RESULT_SUCCESS.value:
                    messagebox.showerror("midi tap pro", "failed to pause of resume screen! error " + str(packet[5]))


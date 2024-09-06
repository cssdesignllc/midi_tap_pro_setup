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

import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tabs.tab_midi_tap_setup import TabMidiTapSetup
from tabs.tab_midi_tap_update import TabMidiTapUpdate
from tabs.tab_midi_tap_stats import TabMidiTapStats
from tabs.tab_midi_tap_display import TabMidiTapDisplay
from midi.midi_port_comm import MidiPortComm

# pip install mido
# pip install python-rtmidi


class MidiTapProApp(tk.Tk):

    def __init__(self):
        super().__init__()

        row = 0

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.comm_manager = MidiPortComm()
        self.midi_out_port_name = StringVar()
        self.midi_in_port_name = StringVar()

        self.title("CSS Designs - MIDI Tap Pro Setup - V1.0")
        self.geometry("1000x600")

        self.grid_columnconfigure(4, weight=1)

        row = row + 1

        # midi port access
        self.tk_open_close_midi_button = ttk.Button(self, text="Open MIDI", command=self.open_close_midi_port)
        self.tk_open_close_midi_button.grid(column=0, row=row, padx=5, pady=5, rowspan=2)

        Label(self, text="MIDI Out Port").grid(row=row, column=1, padx=5, pady=5)

        self.tk_midi_out_ports_combo = ttk.Combobox(self, values=[], state="readonly", textvariable=self.midi_out_port_name, width=40)
        self.tk_midi_out_ports_combo.grid(column=2, row=row, padx=5, pady=5)

        self.tk_refresh_midi_out_ports_button = ttk.Button(self, text="Refresh", command=self.refresh_midi_out_ports)
        self.tk_refresh_midi_out_ports_button.grid(column=3, row=row, padx=5, pady=5)

        row = row + 1

        Label(self, text="MIDI In Port").grid(row=row, column=1, padx=5, pady=5)

        self.tk_midi_in_ports_combo = ttk.Combobox(self, values=[], state="readonly", textvariable=self.midi_in_port_name, width=40)
        self.tk_midi_in_ports_combo.grid(column=2, row=row, padx=5, pady=5)

        self.tk_refresh_midi_in_ports_button = ttk.Button(self, text="Refresh", command=self.refresh_midi_in_ports)
        self.tk_refresh_midi_in_ports_button.grid(column=3, row=row, padx=5, pady=5)

        row = row + 1

        ttk.Separator(self, orient='horizontal').grid(
            row=row, columnspan=5, sticky="we"
        )

        row = row + 1

        self.frame_tabs = tk.Frame(self)
        self.frame_tabs.grid(
            column=0, row=row, columnspan=10, padx=5, pady=5, sticky="ew"
        )

        self.tab_control = ttk.Notebook(self.frame_tabs)
        self.tab_control.enable_traversal()

        self.tab_midi_tap_setup = TabMidiTapSetup(self.tab_control, self.comm_manager)
        self.tab_midi_tap_stats = TabMidiTapStats(self.tab_control, self.comm_manager)
        self.tab_midi_tap_display = TabMidiTapDisplay(self.tab_control, self.comm_manager)
        self.tab_midi_tap_update = TabMidiTapUpdate(self.tab_control, self.comm_manager)

        self.tab_control.grid(column=0, row=0, columnspan=10, padx=5, pady=5, sticky="ew")

        self.refresh_midi_out_ports()
        self.refresh_midi_in_ports()

    def open_close_midi_port(self):
        if self.comm_manager.is_running:
            self.tk_open_close_midi_button.config(text="Open")
            self.tk_refresh_midi_out_ports_button.config(state="enabled")
            self.tk_refresh_midi_in_ports_button.config(state="enabled")
            self.tk_midi_out_ports_combo.config(state="enabled")
            self.tk_midi_in_ports_combo.config(state="enabled")
            self.comm_manager.stop()
        else:
            if self.midi_in_port_name.get() == "":
                messagebox.showerror("error", "no midi in port selected!")
                return
            if self.midi_out_port_name.get() == "":
                messagebox.showerror("error", "no midi out port selected!")
                return
            if self.comm_manager.start(self.midi_out_port_name.get(), self.midi_in_port_name.get(), self.comm_manager_rx_callback):
                self.tk_open_close_midi_button.config(text="Close")
                self.tk_refresh_midi_out_ports_button.config(state="disabled")
                self.tk_refresh_midi_in_ports_button.config(state="disabled")
                self.tk_midi_out_ports_combo.config(state="disabled")
                self.tk_midi_in_ports_combo.config(state="disabled")
            else:
                messagebox.showerror("error", "failed to open port!")

    def midi_out_ports(self):
        return MidiPortComm.get_output_port_names()

    def refresh_midi_out_ports(self):
        self.tk_midi_out_ports_combo.set('')
        self.tk_midi_out_ports_combo.config(values=self.midi_out_ports())
        if len(self.tk_midi_out_ports_combo["values"]) > 0:
            index = 0
            last_mtp_index = 0
            for s in self.tk_midi_out_ports_combo["values"]:
                if 'MIDI Tap Pro' in s:
                    last_mtp_index = index
                index = index + 1
            self.tk_midi_out_ports_combo.current(last_mtp_index)

    def midi_in_ports(self):
        return MidiPortComm.get_input_port_names()

    def refresh_midi_in_ports(self):
        self.tk_midi_in_ports_combo.set('')
        self.tk_midi_in_ports_combo.config(values=self.midi_in_ports())
        if len(self.tk_midi_in_ports_combo["values"]) > 0:
            index = 0
            last_mtp_index = 0
            for s in self.tk_midi_in_ports_combo["values"]:
                if 'MIDI Tap Pro' in s:
                    last_mtp_index = index
                index = index + 1
            self.tk_midi_in_ports_combo.current(last_mtp_index)

    def comm_manager_rx_callback(self, message):
        self.tab_midi_tap_setup.rx_handler(message)
        self.tab_midi_tap_update.rx_handler(message)
        self.tab_midi_tap_stats.rx_handler(message)
        self.tab_midi_tap_display.rx_handler(message)

    def on_closing(self):
        self.comm_manager.stop()
        self.destroy()


if __name__ == "__main__":
    Application = MidiTapProApp()
    Application.mainloop()

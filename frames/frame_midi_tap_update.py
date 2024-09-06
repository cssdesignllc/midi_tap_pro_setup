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

from tkinter import Button, Entry, messagebox
import mido
from frames.frame_base import FrameBase
from midi.midi_port_comm import MidiPortComm
import tkinter as tk
from tkinter import filedialog
from midi.midi_tap_commands import MidiTapCommands
from tkinter.ttk import *


class FrameMidiTapUpdate(FrameBase):
    def __init__(self, parent, comm_manager: MidiPortComm):
        super().__init__(parent, comm_manager)

        self.parent = parent
        self.update_bytes = bytearray()
        self.update_index = 0
        self.in_update = False

        self.grid_columnconfigure(2, weight=1)

        row = 0

        # FIND UPDATE FILE
        self.update_file = tk.StringVar()
        Button(self, text="Find Update File", width=15, command=self.open_update_file).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=65, textvariable=self.update_file, state="readonly").grid(column=1, row=row, sticky='w', padx=5, pady=5)

        row = row + 1

        # UPDATE
        Button(self, text="Update", width=15, command=self.update).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        self.progress = Progressbar(self, value=0, length=400)
        self.progress.grid(column=1, row=row, sticky='w', padx=5, pady=5)

    def open_update_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Update file", "*.upd")])
        if filename == "":
            return
        self.update_file.set(filename)

    def update(self):
        if self.update_file.get() == "":
            messagebox.showerror("midi tap", "no update file chosen")
            return
        bin_file = open(self.update_file.get(), "rb")
        self.update_bytes = bin_file.read()
        self.update_index = 0
        bin_file.close()
        self.progress['maximum'] = len(self.update_bytes)
        self.progress['value'] = 0
        self.send_update_chunk()

    def verify_update_file(self):
        message = MidiTapCommands.build_verify_update_file_command()
        self.comm_manager.write(mido.Message.from_bytes(message))

    def send_update_chunk(self):
        if self.update_index >= len(self.update_bytes):
            print("successfully transmitted update file, verifying...")
            self.verify_update_file()
            return

        self.progress['value'] = self.update_index

        if len(self.update_bytes) - self.update_index > 1000:
            payload_length = 1000
        else:
            payload_length = len(self.update_bytes) - self.update_index

        self.in_update = True

        message = MidiTapCommands.build_update_file_chunk_command(self.update_index, payload_length, self.update_bytes)
        self.comm_manager.write(mido.Message.from_bytes(message))

        self.update_index += payload_length

    def update_code_to_text(self, code):
        if code == 0:
            return "success"
        elif code == 1:
            return "invalid address - update file too large"
        elif code == 2:
            return "no memory - not enough memory to complete update"
        elif code == 3:
            return "invalid length - update chunk size invalid"
        elif code == 4:
            return "update size invalid - update file too large"
        elif code == 5:
            return "checksum invalid"
        elif code == 6:
            return "invalid product type - not a midi tap pro update file"
        else:
            return ""

    def rx_handler(self, message: mido.Message):
        pass
        if self.in_update:
            if message.type == 'sysex':
                packet = message.bytes()
                if len(packet) >= 5:
                    if packet[4] == 0x60:
                        if packet[5] == 0x00:
                            self.send_update_chunk()
                        else:
                            messagebox.showerror("midi tap", "update error " + self.update_code_to_text(packet[5]))
                            self.in_update = False
                    if packet[4] == 0x61:
                        if packet[5] == 0x00:
                            messagebox.showinfo("midi tap", "update file transfer success, power cycle device to complete update")
                        else:
                            messagebox.showerror("midi tap", "update verify error " + self.update_code_to_text(packet[5]))
                        self.in_update = False

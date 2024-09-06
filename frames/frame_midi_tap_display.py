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
import tkinter as tk
from tkinter.ttk import *
from midi.midi_tap_commands import MidiTapCommands
from tkinter import colorchooser


class FrameMidiTapDisplay(FrameBase):
    def __init__(self, parent, comm_manager: MidiPortComm):
        super().__init__(parent, comm_manager)

        self.parent = parent

        self.grid_columnconfigure(11, weight=1)

        row = 0

        # CLEAR SCREEN
        Button(self, text="Clear", width=15, command=self.clear).grid(column=0, row=row, sticky='w', padx=5, pady=5)

        # SEPARATOR
        row = row + 1
        Separator(self, orient='horizontal').grid(
            row=row, columnspan=11, sticky="we"
        )

        row = row + 1

        # SET RECT
        self.rect_x = tk.IntVar(value=50)
        self.rect_y = tk.IntVar(value=50)
        self.rect_width = tk.IntVar(value=100)
        self.rect_height = tk.IntVar(value=100)
        self.rect_color = "#FFFFFF"
        Button(self, text="Set Rect", width=15, command=self.set_rect).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="X").grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.rect_x).grid(column=2, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Y").grid(column=3, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.rect_y).grid(column=4, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Width").grid(column=5, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.rect_width).grid(column=6, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Height").grid(column=7, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.rect_height).grid(column=8, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Color").grid(column=9, row=row, sticky='w', padx=5, pady=5)
        self.button_rect_color = tk.Button(self, text="", width=4, command=self.get_rect_color, bg=self.rect_color)
        self.button_rect_color.grid(column=10, row=row, sticky='w', padx=5, pady=5)

        # SEPARATOR
        row = row + 1
        Separator(self, orient='horizontal').grid(
            row=row, columnspan=11, sticky="we"
        )

        row = row + 1

        # SET LINE
        self.line_x1 = tk.IntVar(value=0)
        self.line_y1 = tk.IntVar(value=0)
        self.line_x2 = tk.IntVar(value=200)
        self.line_y2 = tk.IntVar(value=200)
        self.line_color = "#FFFFFF"
        Button(self, text="Set Line", width=15, command=self.set_line).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="X1").grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.line_x1).grid(column=2, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Y1").grid(column=3, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.line_y1).grid(column=4, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="X2").grid(column=5, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.line_x2).grid(column=6, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Y2").grid(column=7, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.line_y2).grid(column=8, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Color").grid(column=9, row=row, sticky='w', padx=5, pady=5)
        self.button_line_color = tk.Button(self, text="", width=4, command=self.get_line_color, bg=self.line_color)
        self.button_line_color.grid(column=10, row=row, sticky='w', padx=5, pady=5)

        # SEPARATOR
        row = row + 1
        Separator(self, orient='horizontal').grid(
            row=row, columnspan=11, sticky="we"
        )

        row = row + 1

        # SET CIRCLE
        self.circle_x = tk.IntVar(value=100)
        self.circle_y = tk.IntVar(value=100)
        self.circle_radius = tk.IntVar(value=50)
        self.circle_color = "#FFFFFF"
        Button(self, text="Set Circle", width=15, command=self.set_circle).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="X").grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.circle_x).grid(column=2, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Y").grid(column=3, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.circle_y).grid(column=4, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Radius").grid(column=5, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.circle_radius).grid(column=6, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Color").grid(column=7, row=row, sticky='w', padx=5, pady=5)
        self.button_circle_color = tk.Button(self, text="", width=4, command=self.get_circle_color, bg=self.circle_color)
        self.button_circle_color.grid(column=8, row=row, sticky='w', padx=5, pady=5)

        # SEPARATOR
        row = row + 1
        Separator(self, orient='horizontal').grid(
            row=row, columnspan=11, sticky="we"
        )

        row = row + 1

        # SET TEXT
        self.text_x = tk.IntVar(value=0)
        self.text_y = tk.IntVar(value=0)
        self.text_color_foreground = "#FFFFFF"
        self.text_color_background = "#FFFFFF"
        self.text_text = tk.StringVar(value="test text")
        Button(self, text="Set Text", width=15, command=self.set_text).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="X").grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.text_x).grid(column=2, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Y").grid(column=3, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.text_y).grid(column=4, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Foreground Color").grid(column=5, row=row, sticky='w', padx=5, pady=5)
        self.button_text_foreground_color = tk.Button(self, text="", width=4, command=self.get_text_foreground_color, bg=self.text_color_foreground)
        self.button_text_foreground_color.grid(column=6, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Background Color").grid(column=7, row=row, sticky='w', padx=5, pady=5)
        self.button_text_background_color = tk.Button(self, text="", width=4, command=self.get_text_background_color, bg=self.text_color_background)
        self.button_text_background_color.grid(column=8, row=row, sticky='w', padx=5, pady=5)
        row = row + 1
        Label(self, text="Text").grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=50, textvariable=self.text_text).grid(column=2, row=row, sticky='w', padx=5, pady=5, columnspan=4)

        # SEPARATOR
        row = row + 1
        Separator(self, orient='horizontal').grid(
            row=row, columnspan=11, sticky="we"
        )

        row = row + 1

        # DISPLAY TEST
        Button(self, text="Display Test", width=15, command=self.display_test).grid(column=0, row=row, sticky='w', padx=5, pady=5)

    def get_rect_color(self):
        color_code = colorchooser.askcolor(title="Select rectangle color")
        if color_code[0] is None:
            return
        print(color_code[1])
        self.rect_color = color_code[1]
        self.button_rect_color.configure(bg=color_code[1])

    def get_line_color(self):
        color_code = colorchooser.askcolor(title="Select line color")
        if color_code[0] is None:
            return
        print(color_code[1])
        self.line_color = color_code[1]
        self.button_line_color.configure(bg=color_code[1])

    def get_circle_color(self):
        color_code = colorchooser.askcolor(title="Select circle color")
        if color_code[0] is None:
            return
        print(color_code[1])
        self.circle_color = color_code[1]
        self.button_circle_color.configure(bg=color_code[1])

    def get_text_foreground_color(self):
        color_code = colorchooser.askcolor(title="Select text foreground color")
        if color_code[0] is None:
            return
        print(color_code[1])
        self.text_color_foreground = color_code[1]
        self.button_text_foreground_color.configure(bg=color_code[1])

    def get_text_background_color(self):
        color_code = colorchooser.askcolor(title="Select text background color")
        if color_code[0] is None:
            return
        print(color_code[1])
        self.text_color_background = color_code[1]
        self.button_text_background_color.configure(bg=color_code[1])

    def clear(self):
        self.set_rect_parameters(0, 0, 240, 240, 0)

    def rgb(self, r, g, b):
        return ((r << 8) & 0xF800) | ((g << 3) & 0x07E0) | ((b >> 3) & 0x001F)

    def display_test(self):
        self.set_rect_parameters(0, 0, 60, 60, self.rgb(0xFF, 0x00, 0x00))
        self.set_rect_parameters(59, 0, 60, 60, self.rgb(0xAA, 0x00, 0x00))
        self.set_rect_parameters(119, 0, 60, 60, self.rgb(0x77, 0x00, 0x00))
        self.set_rect_parameters(179, 0, 60, 60, self.rgb(0x33, 0x00, 0x00))

        self.set_circle_parameters(30, 90, 30, self.rgb(0x00, 0xFF, 0x00))
        self.set_circle_parameters(90, 90, 30, self.rgb(0x00, 0xAA, 0x00))
        self.set_circle_parameters(150, 90, 30, self.rgb(0x00, 0x77, 0x00))
        self.set_circle_parameters(210, 90, 30, self.rgb(0x00, 0x33, 0x00))

        self.set_rect_parameters(0, 119, 60, 60, self.rgb(0x00, 0x00, 0xFF))
        self.set_rect_parameters(59, 119, 60, 60, self.rgb(0x00, 0x00, 0xAA))
        self.set_rect_parameters(119, 119, 60, 60, self.rgb(0x00, 0x00, 0x77))
        self.set_rect_parameters(179, 119, 60, 60, self.rgb(0x00, 0x00, 0x33))

        self.set_line_parameters(0, 59, 239, 59, self.rgb(0xFF, 0xFF, 0xFF))
        self.set_line_parameters(0, 119, 239, 119, self.rgb(0xFF, 0xFF, 0xFF))
        self.set_line_parameters(0, 179, 239, 179, self.rgb(0xFF, 0xFF, 0xFF))

        self.set_text_parameters(60, 190, self.rgb(0xFF, 0xFF, 0xFF), self.rgb(0x00, 0x00, 0x00), "display test!")

    def hex_color_to_int565(self, hex_color):
        color = int(hex_color.replace("#", ""), 16)
        red = (color >> 16) & 0xFF
        green = (color >> 8) & 0xFF
        blue = (color >> 0) & 0xFF
        return ((red << 8) & 0xF800) | ((green << 3) & 0x07E0) | ((blue >> 3) & 0x001F)

    def set_rect(self):
        color565 = self.hex_color_to_int565(self.rect_color)
        self.set_rect_parameters(self.rect_x.get(), self.rect_y.get(), self.rect_width.get(), self.rect_height.get(), color565)

    def set_text(self):
        color565_foreground = self.hex_color_to_int565(self.text_color_foreground)
        color565_background = self.hex_color_to_int565(self.text_color_background)
        self.set_text_parameters(self.text_x.get(), self.text_y.get(), color565_foreground, color565_background, self.text_text.get())

    def set_line(self):
        color565 = self.hex_color_to_int565(self.line_color)
        self.set_line_parameters(self.line_x1.get(), self.line_y1.get(), self.line_x2.get(), self.line_y2.get(), color565)

    def set_circle(self):
        color565 = self.hex_color_to_int565(self.circle_color)
        self.set_circle_parameters(self.circle_x.get(), self.circle_y.get(), self.circle_radius.get(), color565)

    def set_rect_parameters(self, x, y, width, height, color):
        message = MidiTapCommands.build_set_display_rect_command(x, y, width, height, color)
        self.comm_manager.write(mido.Message.from_bytes(message))

    def set_line_parameters(self, x1, y1, x2, y2, color):
        message = MidiTapCommands.build_set_display_line_command(x1, y1, x2, y2, color)
        self.comm_manager.write(mido.Message.from_bytes(message))

    def set_circle_parameters(self, x, y, radius, color):
        message = MidiTapCommands.build_set_display_circle_command(x, y, radius, color)
        self.comm_manager.write(mido.Message.from_bytes(message))

    def set_text_parameters(self, x, y, color_foreground, color_background, text):
        message = MidiTapCommands.build_set_display_text_command(x, y, color_foreground, color_background, text)
        self.comm_manager.write(mido.Message.from_bytes(message))

    def rx_handler(self, message: mido.Message):
        pass

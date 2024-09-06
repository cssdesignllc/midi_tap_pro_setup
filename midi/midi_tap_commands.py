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

from enum import Enum

CSS_MAN_ID_HI = 0x00
CSS_MAN_ID_MD = 0x02
CSS_MAN_ID_LO = 0x58

SYSEX_START = 0xF0
SYSEX_END = 0xF7


class MidiTapResults(Enum):
    RESULT_SUCCESS = 0x00
    RESULT_UNKNOWN_COMMAND = 0x01
    RESULT_INVALID_COMMAND_LENGTH = 0x02
    RESULT_INVALID_MIDI_PORT = 0x03
    RESULT_INVALID_VALUE = 0x04
    RESULT_INVALID_ADDRESS = 0x05
    RESULT_NO_MEMORY = 0x06
    RESULT_INVALID_LENGTH = 0x07
    RESULT_UPDATE_SIZE_INVALID = 0x08
    RESULT_UPDATE_CHECKSUM_INVALID = 0x09
    RESULT_UPDATE_INVALID_PRODUCT_TYPE = 0x0A


class MidiTapCommands(Enum):
    COMMAND_INVALID = 0x00
    COMMAND_SET_THRU = 0x01
    COMMAND_SET_UART = 0x02
    COMMAND_SET_SCREEN = 0x03
    COMMAND_SET_BACKLIGHT = 0x04
    COMMAND_SAVE_SETTINGS = 0x05
    COMMAND_FACTORY_DEFAULTS = 0x06
    COMMAND_RESET_STATS = 0x07
    COMMAND_GET_STATS = 0x08
    COMMAND_PAUSE_DISPLAY = 0x09
    COMMAND_SET_DISPLAY_RECT = 0x20
    COMMAND_SET_DISPLAY_LINE = 0x21
    COMMAND_SET_DISPLAY_TEXT = 0x22
    COMMAND_SET_DISPLAY_CIRCLE = 0x23
    COMMAND_SET_UPDATE_CHUNK = 0x60
    COMMAND_UPDATE_VALIDATE = 0x61

    @staticmethod
    def build_base_command(command):
        message = bytearray()
        # start byte
        message.append(SYSEX_START)
        # manufacturer id
        message.append(CSS_MAN_ID_HI)
        message.append(CSS_MAN_ID_MD)
        message.append(CSS_MAN_ID_LO)
        # command
        message.append(command)
        return message

    @staticmethod
    def get_command_type(message):
        if len(message) > 4:
            if message[4] == MidiTapCommands.COMMAND_SET_THRU.value:
                return MidiTapCommands.COMMAND_SET_THRU
            elif message[4] == MidiTapCommands.COMMAND_SET_UART.value:
                return MidiTapCommands.COMMAND_SET_UART
            elif message[4] == MidiTapCommands.COMMAND_SET_SCREEN.value:
                return MidiTapCommands.COMMAND_SET_SCREEN
            elif message[4] == MidiTapCommands.COMMAND_SET_BACKLIGHT.value:
                return MidiTapCommands.COMMAND_SET_BACKLIGHT
            elif message[4] == MidiTapCommands.COMMAND_SAVE_SETTINGS.value:
                return MidiTapCommands.COMMAND_SAVE_SETTINGS
            elif message[4] == MidiTapCommands.COMMAND_FACTORY_DEFAULTS.value:
                return MidiTapCommands.COMMAND_FACTORY_DEFAULTS
            elif message[4] == MidiTapCommands.COMMAND_RESET_STATS.value:
                return MidiTapCommands.COMMAND_RESET_STATS
            elif message[4] == MidiTapCommands.COMMAND_GET_STATS.value:
                return MidiTapCommands.COMMAND_GET_STATS
            elif message[4] == MidiTapCommands.COMMAND_PAUSE_DISPLAY.value:
                return MidiTapCommands.COMMAND_PAUSE_DISPLAY
            elif message[4] == MidiTapCommands.COMMAND_SET_DISPLAY_RECT.value:
                return MidiTapCommands.COMMAND_SET_DISPLAY_RECT
            elif message[4] == MidiTapCommands.COMMAND_SET_DISPLAY_LINE.value:
                return MidiTapCommands.COMMAND_SET_DISPLAY_LINE
            elif message[4] == MidiTapCommands.COMMAND_SET_DISPLAY_TEXT.value:
                return MidiTapCommands.COMMAND_SET_DISPLAY_TEXT
            elif message[4] == MidiTapCommands.COMMAND_SET_DISPLAY_CIRCLE.value:
                return MidiTapCommands.COMMAND_SET_DISPLAY_CIRCLE
            elif message[4] == MidiTapCommands.COMMAND_SET_UPDATE_CHUNK.value:
                return MidiTapCommands.COMMAND_SET_UPDATE_CHUNK
            elif message[4] == MidiTapCommands.COMMAND_UPDATE_VALIDATE.value:
                return MidiTapCommands.COMMAND_UPDATE_VALIDATE
            else:
                return MidiTapCommands.COMMAND_INVALID
        else:
            return MidiTapCommands.COMMAND_INVALID

    @staticmethod
    def build_set_thru_command(port: int, enable: bool):
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_SET_THRU.value)
        # thru port
        message.append(port)
        # thru enable or disable
        if enable:
            message.append(0x01)
        else:
            message.append(0x00)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_set_backlight_command(level: int):
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_SET_BACKLIGHT.value)
        # level
        message.append(level)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_set_uart_port_command(port: int):
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_SET_UART.value)
        # port
        message.append(port)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_set_screen_command(screen: int, port: int):
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_SET_SCREEN.value)
        # screen
        message.append(screen)
        # port
        message.append(port)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_save_settings_command():
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_SAVE_SETTINGS.value)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_factory_defaults_command():
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_FACTORY_DEFAULTS.value)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_pause_display_command(pause: bool):
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_PAUSE_DISPLAY.value)
        # pause or resume
        if pause:
            message.append(0x01)
        else:
            message.append(0x00)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_set_display_rect_command(x: int, y: int, width: int, height: int, color: int):
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_SET_DISPLAY_RECT.value)
        # x position
        message.append(x >> 0 & 0x0F)
        message.append(x >> 4 & 0x0F)
        message.append(x >> 8 & 0x0F)
        message.append(x >> 12 & 0x0F)
        # y position
        message.append(y >> 0 & 0x0F)
        message.append(y >> 4 & 0x0F)
        message.append(y >> 8 & 0x0F)
        message.append(y >> 12 & 0x0F)
        # width
        message.append(width >> 0 & 0x0F)
        message.append(width >> 4 & 0x0F)
        message.append(width >> 8 & 0x0F)
        message.append(width >> 12 & 0x0F)
        # height
        message.append(height >> 0 & 0x0F)
        message.append(height >> 4 & 0x0F)
        message.append(height >> 8 & 0x0F)
        message.append(height >> 12 & 0x0F)
        # color
        message.append(color >> 0 & 0x0F)
        message.append(color >> 4 & 0x0F)
        message.append(color >> 8 & 0x0F)
        message.append(color >> 12 & 0x0F)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_set_display_line_command(x1: int, y1: int, x2: int, y2: int, color: int):
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_SET_DISPLAY_LINE.value)
        # x1
        message.append(x1 >> 0 & 0x0F)
        message.append(x1 >> 4 & 0x0F)
        message.append(x1 >> 8 & 0x0F)
        message.append(x1 >> 12 & 0x0F)
        # y1
        message.append(y1 >> 0 & 0x0F)
        message.append(y1 >> 4 & 0x0F)
        message.append(y1 >> 8 & 0x0F)
        message.append(y1 >> 12 & 0x0F)
        # x2
        message.append(x2 >> 0 & 0x0F)
        message.append(x2 >> 4 & 0x0F)
        message.append(x2 >> 8 & 0x0F)
        message.append(x2 >> 12 & 0x0F)
        # y2
        message.append(y2 >> 0 & 0x0F)
        message.append(y2 >> 4 & 0x0F)
        message.append(y2 >> 8 & 0x0F)
        message.append(y2 >> 12 & 0x0F)
        # color
        message.append(color >> 0 & 0x0F)
        message.append(color >> 4 & 0x0F)
        message.append(color >> 8 & 0x0F)
        message.append(color >> 12 & 0x0F)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_set_display_circle_command(x: int, y: int, radius: int, color: int):
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_SET_DISPLAY_CIRCLE.value)
        # x position
        message.append(x >> 0 & 0x0F)
        message.append(x >> 4 & 0x0F)
        message.append(x >> 8 & 0x0F)
        message.append(x >> 12 & 0x0F)
        # y position
        message.append(y >> 0 & 0x0F)
        message.append(y >> 4 & 0x0F)
        message.append(y >> 8 & 0x0F)
        message.append(y >> 12 & 0x0F)
        # radius
        message.append(radius >> 0 & 0x0F)
        message.append(radius >> 4 & 0x0F)
        message.append(radius >> 8 & 0x0F)
        message.append(radius >> 12 & 0x0F)
        # color
        message.append(color >> 0 & 0x0F)
        message.append(color >> 4 & 0x0F)
        message.append(color >> 8 & 0x0F)
        message.append(color >> 12 & 0x0F)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_set_display_text_command(x: int, y: int, color_foreground: int, color_background: int, text: str):
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_SET_DISPLAY_TEXT.value)
        # x
        message.append(x >> 0 & 0x0F)
        message.append(x >> 4 & 0x0F)
        message.append(x >> 8 & 0x0F)
        message.append(x >> 12 & 0x0F)
        # y
        message.append(y >> 0 & 0x0F)
        message.append(y >> 4 & 0x0F)
        message.append(y >> 8 & 0x0F)
        message.append(y >> 12 & 0x0F)
        # foreground color
        message.append(color_foreground >> 0 & 0x0F)
        message.append(color_foreground >> 4 & 0x0F)
        message.append(color_foreground >> 8 & 0x0F)
        message.append(color_foreground >> 12 & 0x0F)
        # background color
        message.append(color_background >> 0 & 0x0F)
        message.append(color_background >> 4 & 0x0F)
        message.append(color_background >> 8 & 0x0F)
        message.append(color_background >> 12 & 0x0F)
        # text
        for i in range(len(text)):
            message.append(ord(text[i]) & 0x7F)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_reset_stats_command():
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_RESET_STATS.value)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_get_stats_command():
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_GET_STATS.value)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_verify_update_file_command():
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_UPDATE_VALIDATE.value)
        # end byte
        message.append(SYSEX_END)
        return message

    @staticmethod
    def build_update_file_chunk_command(update_index: int, data_length: int, file_data: bytearray):
        message = MidiTapCommands.build_base_command(MidiTapCommands.COMMAND_SET_UPDATE_CHUNK.value)
        # file offset - broken into nibbles
        message.append(update_index >> 0 & 0x0F)
        message.append(update_index >> 4 & 0x0F)
        message.append(update_index >> 8 & 0x0F)
        message.append(update_index >> 12 & 0x0F)
        message.append(update_index >> 16 & 0x0F)
        message.append(update_index >> 20 & 0x0F)
        message.append(update_index >> 24 & 0x0F)
        message.append(update_index >> 28 & 0x0F)
        for i in range(data_length):
            message.append(file_data[update_index] >> 0 & 0x0F)
            message.append(file_data[update_index] >> 4 & 0x0F)
            update_index += 1
        # end byte
        message.append(SYSEX_END)
        return message

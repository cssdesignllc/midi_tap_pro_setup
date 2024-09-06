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

import time
import mido
import threading
import rtmidi


class MidiPortComm:

    def __init__(self):
        self.rx_callback = object()
        self.is_running = False
        self.input_port = mido.ports.BaseInput()
        self.output_port = mido.ports.BaseOutput()

    @staticmethod
    def get_output_port_names():
        return mido.get_output_names()

    @staticmethod
    def get_input_port_names():
        return mido.get_input_names()

    def cb(self, message):
        print(message)
        #self.rx_callback(message)

    def start(self, output_port_name, input_port_name, rx_callback):
        if self.is_running:
            print("failed to start! already connected!")
            return True
        self.rx_callback = rx_callback
        try:
            self.output_port = mido.open_output(output_port_name)
            self.input_port = mido.open_input(input_port_name)
            #self.is_running = True
            thread_handle = threading.Thread(target=self.comm_thread)
            thread_handle.start()
        except:
            print("open exception!")
            return False
        return True

    def stop(self):
        if self.is_running:
            self.is_running = False
            try:
                self.input_port.close()
                self.output_port.close()
            except:
                print("close exception!")

    def write(self, message: mido.Message):
        if self.output_port.closed:
            print("midi out port closed!")
            return
        self.output_port.send(message)

    def comm_thread(self):
        self.is_running = True
        print("enter client thread")

        try:
            while self.is_running:
                message = self.input_port.receive(block=False)
                if message is None:
                    time.sleep(.01)
                else:
                    try:
                        self.rx_callback(message)
                    except:
                        print('exception in rx callback')
        except:
            print("read exception!")

        self.is_running = False

        print("leave client thread")

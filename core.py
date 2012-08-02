#!/usr/bin/python
import sys, threading, time, argparse
import dmx, color

NUM_STRANDS = 24 # Number of LED Strands
FREQUENCY   = 1  # Number of times per second to update

timeout = 1.0 / FREQUENCY

bright_rainbow = color.rainbow_palette(NUM_STRANDS, 1, 1)
pastel_rainbow = color.rainbow_palette(NUM_STRANDS, 0.33, 1)

palettes = [
    bright_rainbow,
    pastel_rainbow # todo: more stuff
]

class Program:
    def __init__(self, **kwargs):
        self.widget = dmx.Widget(port)
        self.timeout = 1/ freq
    
    def run(self):
        self.tick()
        time.sleep(60)
        
    def tick(self):
        colors = pastel_rainbow # todo: we do our crazy sequence math here
        
        packet = dmx.Packet(colors)
        self.widget.send_dmx(packet)
        threading.Timer(timeout, self.tick).start()


def main():
    parser = argparse.ArgumentParser(description='Run the Idaho CORE project lighting script')
    parser.add_argument('port', default='fake', help='The name of the serial port to run on (fake if you want to print to screen)')
    parser.add_argument('-f', '--freq', metavar='Hz', default=1, type=int, help='The frequency, in Hertz, to run the update loop.')
    options = parser.parse_args()
    program = Program(options)
    program.run()

if __name__ == "__main__":
    sys.exit(main())

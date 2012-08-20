#!/usr/bin/python
import sys, threading, time, datetime, argparse
import dmx, color

NUM_STRANDS = 4 # Number of LED Strands

palettes = {
    'off'           : color.MonoPalette(NUM_STRANDS, color.Black),
    'bright_rainbow': color.RainbowPalette(NUM_STRANDS, 1, 1),
	'pastel_rainbow': color.RainbowPalette(NUM_STRANDS, 0.33, 1),
    'christmas'     : color.CandyPalette(NUM_STRANDS, [color.Red, color.Green]),
    'red_stripe'    : color.StripePalette(NUM_STRANDS, color.Red, color.Black),
    'blue_stripe'   : color.StripePalette(NUM_STRANDS, color.Blue, color.Black),
}

effects = dict()
effects['fast_red_stripe']  = color.Rotator(palettes['red_stripe'], 100)
effects['slow_blue_stripe'] = color.Rotator(palettes['blue_stripe'], 250)
effects['test']             = color.AdditionEffect(effects['fast_red_stripe'],
        effects['slow_blue_stripe'])

sequences = dict()
sequences.update(palettes)
sequences.update(effects)

class Program:
    def __init__(self, port, sequence, freq):
        self.widget = dmx.Widget(port)
        self.timeout = 1.0/float(freq)
        self.elapsed = 0.0
        self.lastTime = datetime.datetime.now()

        if(sequence not in sequences):
            print('Could not find sequenced named %s' % sequence)
            sys.exit(1)
        self.sequence = sequences[sequence]
        print('Running %s sequence at timeout of %d seconds.' % (sequence, self.timeout))
    
    def run(self):
        while True:
            current = datetime.datetime.now()
            delta = (current - self.lastTime).total_seconds() * 1000
            self.elapsed += delta
            palette = self.sequence(self.elapsed, delta)
            self.widget.send_palette(palette)
            time.sleep(self.timeout)

def main():
    parser = argparse.ArgumentParser(description='Run the Idaho CORE project lighting script')
    parser.add_argument('port', help='The name of the serial port to run on (fake if you want to print to screen)')
    parser.add_argument('-f', '--freq', metavar='Hz', default=1, type=int, help='The frequency, in Hertz, to run the update loop.')
    parser.add_argument('sequence', default='all', help='The sequence to run.')
    options = parser.parse_args()

    program = Program(options.port, options.sequence, options.freq)
    return program.run()

if __name__ == "__main__":
    sys.exit(main())

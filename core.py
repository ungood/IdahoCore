#!/usr/bin/python
import sys, threading, time, datetime, argparse
import dmx, color

NUM_STRANDS  = 24    # Number of LED Strands
LIMIT_SCALE = 0.65 # The max power as a percentage (0-1.0) of all-white power draw to limit

palettes = {
    'off'           : color.MonoPalette(NUM_STRANDS, color.Black),
    'red'           : color.MonoPalette(NUM_STRANDS, color.Red),
    'green'         : color.MonoPalette(NUM_STRANDS, color.Green),
    'blue'          : color.MonoPalette(NUM_STRANDS, color.Blue),
    'white'         : color.MonoPalette(NUM_STRANDS, color.White),
    'bright_rainbow': color.RainbowPalette(NUM_STRANDS, 1, 1),
    'pastel_rainbow': color.RainbowPalette(NUM_STRANDS, 0.33, 1),
    'christmas'     : color.CandyPalette(NUM_STRANDS, [color.Red, color.Green]),
    'barber_pole'   : color.CandyPalette(NUM_STRANDS, [color.Black, color.Black, color.White]),
    'red_stripe'    : color.StripePalette(NUM_STRANDS, color.Red, color.Black),
    'green_stripe'  : color.StripePalette(NUM_STRANDS, color.Green, color.Black),
    'blue_stripe'   : color.StripePalette(NUM_STRANDS, color.Blue, color.Black),
    'cylon'         : color.FadePalette(NUM_STRANDS, color.Red, color.Black)
}

tests = dict()
tests['red_test'] = color.Rotator(palettes['red_stripe'], 2000 / NUM_STRANDS)
tests['green_test'] = color.Rotator(palettes['green_stripe'], 1800 /
        NUM_STRANDS)
tests['blue_test'] = color.Rotator(palettes['blue_stripe'], -2000 / NUM_STRANDS)
tests['rainbow_test'] = color.Rotator(palettes['bright_rainbow'], -250)
tests['sine_test'] = color.Rotator(palettes['blue_stripe'], color.Sine(100, 1000,
    30000))
tests['barber_pole_test'] = color.Rotator(palettes['barber_pole'], 500)
tests['layered_test'] = color.MultiplyEffect(tests['barber_pole_test'],
        tests['rainbow_test'])
tests['beat_test'] = color.BlendEffect(palettes['off'], palettes['red'],
        color.Beat(0, 1, 1000, 1000))
tests['blend_test'] = color.BlendEffect(palettes['bright_rainbow'],
        tests['rainbow_test'],
        color.Sine(0, 1, 5000))
tests['big_test'] = color.BlendEffect(tests['beat_test'],
        color.BlendEffect(tests['red_test'],
            color.BlendEffect(tests['blue_test'], tests['green_test'], 0.5),
            0.5), 0.50)

effects = dict()
effects['rotating_rainbow'] = color.Rotator(palettes['bright_rainbow'],
        color.Sine(-100, 100, 20 * 1000))
effects['fast_red_stripe']  = color.Rotator(palettes['red_stripe'], 100)
effects['slow_blue_stripe'] = color.Rotator(palettes['blue_stripe'], 250)
effects['test']             = color.AdditionEffect(effects['fast_red_stripe'], effects['slow_blue_stripe'])
all_effects = [v for (k, v) in effects.iteritems()]


sequences = dict()
sequences.update(tests)
sequences.update(palettes)
sequences.update(effects)

# This is the main sequence to run - it blends together all the effects.
# Blends between effects, the second parameter is the amount of time to leave
# one running, the third parameter is the time to crossover.
sequences['main'] = color.Blender(all_effects, color.Uniform(10 * 1000, 30 *
    1000), 2000)

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
        self.sequence = color.LimitingEffect(self.sequence, LIMIT_SCALE)
        print('Running %s sequence at timeout of %f seconds.' % (sequence, self.timeout))
    
    def run(self, runTime):
        while runTime <= 0 or self.elapsed < runTime:
            current = datetime.datetime.now()
            delta = (current - self.lastTime).total_seconds() * 1000
            self.lastTime = current
            self.elapsed += delta
            palette = self.sequence(self.elapsed, delta)
            self.widget.send_palette(palette)
            time.sleep(self.timeout)

def main():
    parser = argparse.ArgumentParser(description='Run the Idaho CORE project lighting script')
    parser.add_argument('-p', '--port', default='/dev/ttyUSB0', help='The name of the serial port to run on (fake if you want to print to screen)')
    parser.add_argument('-f', '--freq', metavar='Hz', default=30, type=int, help='The frequency, in Hertz, to run the update loop.')
    parser.add_argument('sequence', default='main', help='The sequence to run.')
    parser.add_argument('-t', '--time', metavar='ms', default=0, type=int, help='The amount of time, in ms, to run the program before closing.  Will run forever if 0.')
    options = parser.parse_args()

    program = Program(options.port, options.sequence, options.freq)
    return program.run(options.time)

if __name__ == "__main__":
    sys.exit(main())


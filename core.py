import sys, threading, time
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
    def __init__(self, port):
        self.widget = dmx.Widget(port)
    
    def run(self):
        self.tick()
        time.sleep(60)
        
    def tick(self):
        colors = pastel_rainbow # todo: we do our crazy sequence math here
        
        packet = dmx.Packet(colors)
        self.widget.send_dmx(packet)
        threading.Timer(timeout, self.tick).start()

#def run(portName):
 #   print "Running..."
 #   tick()
    #widget = dmx.Widget(portName)
    #packet = dmx.Packet(bright_rainbow)
    #widget.send_dmx(packet)

def main(argv=None):
    try:
        port = argv[1]
        program = Program(port)
    except:
        print "Usage: python core.py {portname}"
        return 1
    program.run()

if __name__ == "__main__":
    sys.exit(main(sys.argv))

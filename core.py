#!/usr/bin/python
import sys, threading, time, argparse
import dmx, color

NUM_STRANDS = 4 # Number of LED Strands
#FREQUENCY   = 1  # Number of times per second to update

#timeout = 1.0 / FREQUENCY

bright_rainbow = color.rainbow_palette(NUM_STRANDS, 1, 1)
pastel_rainbow = color.rainbow_palette(NUM_STRANDS, 0.33, 1)

palettes = [
    bright_rainbow,
    pastel_rainbow # todo: more stuff
]

class Program:
    def __init__(self, port, freq):
        self.widget = dmx.Widget(port)
        self.timeout = 1.0/float(freq)
    
    def run(self):
	print 'Running at timeout of '+str(self.timeout)+' seconds...'
	#Removed timer to simplify for my debugging -JB
        #self.tick()
        #time.sleep(60)
	

	#Example Sequence #1: Create a few palettes and rotate them
	#		      at different speeds.
        p1=[color.Blue,color.Black,color.Black,color.Black]
        p2=[color.Red,color.Black,color.Black,color.Black]
	#p3=color.rainbow_palette(NUM_STRANDS,1.0,1.0)
	self.spinPalettes=[p1,p2]

	#Create one rotator for each palette.
	r1=color.Rotator(color.Constant(250))
	r2=color.Rotator(color.Constant(100))
	#r3=color.Rotator(color.Constant(5000))
	self.spinRotators=[r1,r2]

	self.elapsed=0.0
	self.delta=self.timeout*1000

	while True:
	   #track the total elapsed time.  Rotators need to know.
           self.elapsed+=self.delta
	   
	   #get the first rotated palette
	   merged=self.spinRotators[0].update(self.spinPalettes[0],self.elapsed,self.delta)
	   
	   #add all other rotated palettes on top of the first one
	   for i in range(1,len(self.spinRotators)):
              nextP=self.spinRotators[i].update(self.spinPalettes[i],self.elapsed,self.delta)
	      merged=color.blend_palettes(merged,nextP,1.0/(len(self.spinRotators)+1))

	   self.widget.send_Palette(merged)
	   time.sleep(self.timeout)

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
    #print 'Port received: '+options.port
    #print 'Frequency received: '+str(options.freq)
    program = Program(options.port,options.freq)
    program.run()

if __name__ == "__main__":
    sys.exit(main())

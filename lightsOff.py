#!/usr/bin/python
import sys
import dmx, color

NUM_STRANDS = 4  # Number of LED Strands


#This file turns off all the strands.
if __name__ == "__main__":
   widget=dmx.Widget('/dev/ttyUSB0')
   widget.send_Palette(color.mono_palette(NUM_STRANDS, color.Black))


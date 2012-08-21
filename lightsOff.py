#!/usr/bin/python
import sys
import dmx, color

NUM_STRANDS = 24  # Number of LED Strands

widget=dmx.Widget('/dev/ttyUSB0')
widget.send_dmx(dmx.Packet(color.MonoPalette(NUM_STRANDS, color.Black)(0, 0)))


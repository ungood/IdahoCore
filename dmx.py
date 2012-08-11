import sys

try:
    from serial import Serial
except:
    from fakes import Serial
    print("pySerial package NOT FOUND")


SOM = b'\x7E'
EOM = b'\xE7'
SC =  b'\x00'
    
LABEL_OUTPUT_ONLY_SEND_DMX = b'\x06'


class Widget:
    """Class to interface with the USBDMX Pro Widget"""
        
    def __init__(self, port):
        try:
            self.serialPort = Serial(port=port, baudrate=57600, timeout=1)
            # self.serialPort = serial.Serial(port=port, baudrate=57600, timeout=1)
            print("Connected to USBDMX on port '%s'" % (self.serialPort.portstr))
        except:
            print("ERROR: Could not open port '%s'" % port)
            sys.exit(1)
    
    def transmit(self, label, data):
        data_size = len(data)
        header = bytearray(label)
        header.append(int(data_size & 0xFF))
        header.append(int((data_size >> 8) & 0xFF)) 
        message = SOM + header + data + EOM
        self.serialPort.write(message)
    
    def send_dmx(self, packet):
        msg = SC + bytes(packet.data)
        self.transmit(LABEL_OUTPUT_ONLY_SEND_DMX, msg)


class Packet:
    def __init__(self, colors):
        self.data = bytearray()
        for color in colors:
            r, g, b = color
            self.data.append(int(r * 255))
            self.data.append(int(g * 255))
            self.data.append(int(b * 255))
            

if __name__ == "__main__":
    widget = Widget('/dev/ttyUSB0')
    import color
    import time
    while True:
        widget.send_dmx(Packet[color.Red, color.Green, color.Blue])
        time.sleep(1)
        widget.send_dmx(Packet[color.Green, color.Blue, color.Red])
        time.sleep(1)
        widget.send_dmx(Packet[color.Blue, color.Red, color.Green])
        time.sleep(1)

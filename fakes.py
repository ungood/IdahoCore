class Serial:
    def __init__(self, **kwargs):
        print "Opening FAKE Serial Port"
        self.portstr = kwargs['port']

    def write(self, data):
        print "FAKE: " + ' '.join(["%02X" % byte for byte in bytearray(data)])


if __name__ == "__main__":
    ser = Serial(port='xyz')
    ser.write("Testing Fake Serial")

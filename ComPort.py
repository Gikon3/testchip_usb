import serial


class ComPort:
    def __init__(self, portname="COM11", baundrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE, timeout=4):
        self.PORTNAME = portname
        self.BAUNDRATE = baundrate
        self.BYTESIZE = bytesize
        self.PARITY = parity
        self.STOPBITS = stopbits
        self.TIMEOUT = timeout

        self.port = serial.Serial(
            port=self.PORTNAME,
            baudrate=self.BAUNDRATE,
            bytesize=self.BYTESIZE,
            parity=self.PARITY,
            stopbits=self.STOPBITS,
            timeout=self.TIMEOUT)

        print(self.PORTNAME, "is Open")

    def read(self):
        msg = bytearray(self.port.read(4)).hex().upper()

        return "{0:2s}{1:2s}{2:2s}{3:2s}".format(msg[-2:], msg[-4:-2], msg[-6:-4], msg[-8:-6])

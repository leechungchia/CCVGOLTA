from time import sleep
import serial
# these codes are for bluetooth
# hint: please check the function "sleep". how does it work?

class bluetooth:
    def __init__(self):
        self.ser = serial.Serial()

    def do_connect(self,port,baudrate,timeout):
        self.ser.baudrate = baudrate
        self.ser.port = port
        self.ser.timeout = timeout
        self.ser.open()
        if self.ser.is_open:
            return "doconnect"
        #TODO: Connect the port with Serial. A clear description for exception may be helpful.
        return "nonconnect"

    def disconnect(self):
        self.ser.close()
        if not self.ser.is_open:
            return "disconnect"
        return "still connecting"

    def SerialWrite(self,output):
        send = output.encode("utf-8")
        self.ser.write(send)

    def SerialReadString(self):
        """
        waiting = self.ser.in_waiting
        rv = self.ser.read()
        """

        rv = self.ser.readline().decode("utf-8")
        rv = rv.rstrip('\n')
        print(rv)
        #print(rv)
        #time.sleep(0.5)
        #TODO: Get the information from Bluetooth. Notice that the return type should be transformed into hex. 
        return rv

    def SerialReadByte(self):
        rv = (self.ser.readline()).hex().rstrip("0a")
        print(rv)
        #print(rv)
        #TODO: Get the UID from bytes. Notice that the return type should be transformed into hex. 
        return rv
"""
a = bluetooth()
print(a.do_connect("COM5",9600,2.0))
#a.SerialWrite("T")
while True:
    a.SerialReadByte()
"""
a = min([[1,2,3],[1,2]])
print(a)


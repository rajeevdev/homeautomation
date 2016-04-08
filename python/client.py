#!/usr/bin/env python

import socket
import sys
import time
import select

moduleId = "00:00:00:00:00:00"
pins8 = [4,5,0,2,16,14,12,13]
pinState = [1,1,1,1,1,1,1,1]
pins2 = [0,2]
totalPins = 8
currentPins = []

class Client(object):
    def __init__(self):
        self.connected = False
        #self.server_address = ('192.168.42.1', 9000)
        self.server_address = ('127.0.0.1', 9000)
        print "Client started with:"
        print "moduleId: " + moduleId
        print "Total pins: " + str(totalPins)

    def read(self, timeout = 10):
        packet = ""
        data = ""
        start = time.time()
        while True:
            try:
                delay = .5
                (readyRead, readyWrite, readyException) = select.select([self.socket], [], [], delay)
                if (readyRead):
                    data += self.socket.recv(2048)
                    startIndex = data.find("[");
                    endIndex = data.find("]");
                    if (startIndex >= 0 and endIndex >= 0):
                        packet = data[startIndex:endIndex+1]
                        data = data[endIndex+1:]
                        print "Received packet : " + packet
                        break;
                if (time.time() - start) > timeout:
                    print "Complete packet not received: " + data
                    break
            except:
                raise;

        return packet;
    
    def write(self, data):
        print "Data sent : " + data
        self.socket.send(data)

    def loop(self):
        while True:
            try:
                if (self.connected == False):
                    print 'Connecting to %s port %s' % self.server_address
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket.connect(self.server_address)
            except:
                print '#### Could not connect to server'
                self.socket.close()
                self.connected = False
                time.sleep(5)
            else:
                self.connected  = True
            
            if (self.connected):            
                try:                    
                    (readyRead, readyWrite, readyException) = select.select([self.socket], [], [], .5)
                    if (readyRead):
                        command = self.read();
                        if (command == "[GET /moduleId]"):
                            time.sleep(.5)
                            self.write("[/moduleId/" + moduleId + "]")

                        elif (command == "[GET /pins]"):
                            time.sleep(.5)
                            pinsStr = ",".join([str(pin) for pin in currentPins])
                            self.write("[/pins/" + pinsStr + "]")
                            
                        elif (command.find("[GET /gpio") >= 0):
                            pinStr = command
                            pinStr = pinStr.replace("[GET /gpio", "")
                            pinStr = pinStr.replace("]", "")
                            pin = int(pinStr)
                            time.sleep(.5)
                            if (pin in currentPins):
                                index = currentPins.index(pin)
                                self.write("[/gpio" + pinStr + "/" + str(pinState[index]) + "]")
                            else:
                                self.write("[NOK]")

                        elif (command.find("[SET /gpio") >= 0):
                            temp = command
                            temp = temp.replace("[SET /gpio", "")
                            temp = temp.replace("]", "")
                            pin = int(temp[:temp.index("/")])
                            value = int(temp[temp.index("/") + 1:])
                            print pin
                            print value
                            time.sleep(.5)
                            if (pin in currentPins):
                                index = currentPins.index(pin)
                                pinState[index] = value
                                self.write("[/gpio" + str(pin) + "/" + str(pinState[index]) + "]")
                            else:
                                self.write("[NOK]")

                except:
                    self.socket.close()
                    self.connected = False
                    time.sleep(5)
         
            time.sleep(.5)

if (len(sys.argv) > 1):
    moduleId = sys.argv[1]
if (len(sys.argv) > 2):
    totalPins = int(sys.argv[2])
currentPins = pins8
if (totalPins == 2):
    currentPins = pins2
    
cl = Client()
cl.loop()

#str = ",".join([str(pin) for pin in currentPins])
#print str

# print pinState
# command = "[/gpio12/0]"
# temp = command
# temp = temp.replace("[/", "")
# temp = temp.replace("]", "")
# print temp[:temp.index("/")]
# print temp[temp.index("/") + 1:]
# temp = temp.replace("[SET /gpio", "")
# temp = temp.replace("]", "")
# pin = int(temp[:temp.index("/")])
# value = int(temp[temp.index("/") + 1:])
# if (pin in currentPins):
    # index = currentPins.index(pin)
    # pinState[index] = value
    # print "[/gpio" + str(pin) + "/" + str(pinState[index]) + "]"
# else:
    # print "[NOK]"
    
# print pinState
# print pin
# if (pin in currentPins):
    # index = currentPins.index(pin)
    # print "[/gpio" + pinStr + "/" + str(pinState[index]) + "]"
# else:
    # print "[NOK]"

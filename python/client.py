#!/usr/bin/env python

import socket
import sys
import time
import select

class Client(object):
    def __init__(self, moduleId = "00:00:00:00:00:00"):
        self.connected = False
        #self.server_address = ('192.168.42.1', 9000)
        self.server_address = ('127.0.0.1', 9000)
        self.gpio0 = "1";
        self.gpio2 = "1";
        self.moduleId = moduleId;
        print "Client started with moduleId: " + moduleId

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
                            self.write("[/moduleId/" + self.moduleId + "]")
                        elif (command == "[GET /gpio0]"):
                            time.sleep(.5)
                            self.write("[/gpio0/" + self.gpio0 + "]")
                        elif (command == "[GET /gpio2]"):
                            time.sleep(.5)
                            self.write("[/gpio2/" + self.gpio2 + "]")
                        elif (command == "[SET /gpio0/0]" or command == "[SET /gpio0/1]"):
                            self.gpio0 = command.replace("[SET /gpio0/", "")
                            self.gpio0 = self.gpio0.replace("]", "")
                            time.sleep(.5)
                            reply = command.replace("SET ", "")
                            self.write(reply)
                        elif (command == "[SET /gpio2/0]" or command == "[SET /gpio2/1]"):
                            self.gpio2 = command.replace("[SET /gpio2/", "")
                            self.gpio2 = self.gpio2.replace("]", "")
                            time.sleep(.5)
                            reply = command.replace("SET ", "")
                            self.write(reply)

                except:
                    self.socket.close()
                    self.connected = False
                    time.sleep(5)
         
            time.sleep(.5)

moduleId = "00:00:00:00:00:00"
if (len(sys.argv) > 1):
    moduleId = sys.argv[1]
cl = Client(moduleId)
cl.loop()
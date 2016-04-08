import socket
import threading
import select
import time
import json
import logger
import config

# COMMANDS:
# ---------
# [GET /moduleId]
# [/moduleId/48-2C-6A-1E-59-3D]
#
# [GET /pins]
# [/pins/4,5,0,2,16,14,12,13]
# or
# [/pins/0,2]

# [GET /gpio0]
# [/gpio0/0]
#
# [GET /gpio2]
# [/gpio2/0]
#
# [SET /gpio0/1]
# [/gpio0/1]
#
# [SET /gpio0/0]
# [/gpio0/0]
#
# [SET /gpio2/1]
# [/gpio2/1]
#
# [SET /gpio2/0]
# [/gpio2/0]

class ClientThread(threading.Thread):
    def __init__(self, server, id, ip, port, socket):
        threading.Thread.__init__(self)
        self.server = server
        self.id = id
        self.ip = ip
        self.port = port
        self.socket = socket
        self.moduleId = ""
        self.pins = []
        self.writeBuffer = ""
        self.success = True
        self.event = None
        self.writeLock = threading.Lock()
        logger.info("Creating thread with ID '" + str(id) + "' for " + ip + ":" + str(port))

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
                        data = ""
                        #data = data[endIndex+1:]
                        logger.debug("Received packet : " + packet)
                        
                        break;
                if (time.time() - start) > timeout:
                    logger.debug("Complete packet not received: " + data)
                    data = ""
                    break
            except:
                raise;

        return packet;
    
    def getModuleId(self):
        return self.moduleId;

    def setSwitchState(self, switchId, status):
        if (status == "0"):
            status = "1"
        else:
            status = "0"

        self.event = threading.Event()
        logger.debug("Appending new command in thread")
        self.writeLock.acquire();
        self.success = True
        self.writeBuffer = "[SET /" + switchId + "/" + status + "]"
        self.writeLock.release();
        self.event.wait()
        logger.debug("Command processing complete")
        return self.success
        
    def run(self):
        try:
            logger.info("Connection from : " + self.ip + ":" + str(self.port))
            logger.info("Receiving module ID")
            self.socket.send("[GET /moduleId]")
            moduleIdReply = self.read();
            moduleIdReply = moduleIdReply.replace("[/moduleId/", "")
            self.moduleId = moduleIdReply.replace("]", "")
            self.moduleId = self.moduleId.replace(":", "-")
            time.sleep(1)

            logger.info("Receiving pins")
            self.socket.send("[GET /pins]")
            pinsReply = self.read();
            pinsReply = pinsReply.replace("[/pins/", "")
            pinsReply = pinsReply.replace("]", "")
            self.pins = [int(pin) for pin in pinsReply.split(",")]
            time.sleep(1)

            for pin in self.pins:
                gpioName = "gpio" + str(pin)
                logger.info("Receiving " + gpioName + " state")
                self.socket.send("[GET /" + gpioName + "]")
                reply = self.read();
                reply = reply.replace("[/" + gpioName + "/", "")
                gpioValue = reply.replace("]", "")
                config.updateSwitch(self.moduleId, gpioName, gpioValue)
                time.sleep(1)
            config.updateModule(self.moduleId, "1");
            #logger.info(config.getFormattedString())
            start = time.time()
            
            while True:
                self.writeLock.acquire();
                currentCommand = self.writeBuffer;
                self.writeBuffer = "";
                self.writeLock.release();
                if currentCommand:
                    logger.debug("Sending command: " + currentCommand)
                    self.socket.send(currentCommand)
                    reply = self.read();
                    if (reply.find("[/gpio") >= 0):
                        reply = reply.replace("[/", "")
                        reply = reply.replace("]", "")
                        gpioName = reply[:reply.index("/")]
                        gpioValue = reply[reply.index("/") + 1:]
                        config.updateSwitch(self.moduleId, gpioName, gpioValue)
                    else:
                        self.success = False
                        logger.error("Error changing state")
                    self.event.set();
                    logger.debug("Notify processing complete")
                
                # Dummy read
                if (time.time() - start) > 5:
                    logger.info("Checking connection status !!!")
                    self.socket.send("[GET /moduleId]")
                    moduleIdReply = self.read();
                    start = time.time()

                time.sleep(.5)

        except socket.error, e:
            logger.error("Socket error")
        except:
            logger.error("Socket error")
        
        self.server.removeThread(self.id)
        config.updateModule(self.moduleId, "0");
        logger.info("Client disconnected...")
        #logger.info(config.getFormattedString())

class Server(threading.Thread):
    def __init__(self, port):
        logger.info("Device Server object created")
        threading.Thread.__init__(self)
        self.port = port
        self.threadDict = dict()
        self.idCounter = 1
        self.dictLock = threading.Lock()
        
    def setSwitchState(self, moduleId, switchId, status):
        self.dictLock.acquire();
        thread_temp = None;
        for id, thread in self.threadDict.iteritems():
            if (thread.getModuleId() == moduleId):
                thread_temp = thread
                break
        self.dictLock.release();
        
        if (thread_temp):
            return thread.setSwitchState(switchId, status)
        return False

    def removeThread(self, id):
        self.dictLock.acquire();
        del self.threadDict[id];
        self.dictLock.release();
        
    def run(self):
    
        logger.info("Starting server on port: " + str(self.port))
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpsock.bind(("0.0.0.0", self.port))
        tcpsock.listen(5)
        
        while True:
            logger.info("Listening for incoming connections...")
            (clientsock, (ip, port)) = tcpsock.accept()
            newthread = ClientThread(self, self.idCounter, ip, port, clientsock)
            newthread.daemon = True
            newthread.start()
            self.dictLock.acquire()
            self.threadDict[self.idCounter] = newthread
            logger.info("Total connection:" + str(len(self.threadDict)) + "\n")
            self.dictLock.release()
            self.idCounter = self.idCounter + 1

import socket
import threading
import select
import time
import json
import logger
import config

class ClientThread(threading.Thread):
    def __init__(self, server, id, ip, port, socket):
        threading.Thread.__init__(self)
        self.server = server
        self.id = id
        self.ip = ip
        self.port = port
        self.socket = socket
        self.moduleId = ""
        self.writeBuffer = ""
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
                        data = data[endIndex+1:]
                        logger.info("Received packet : " + packet)
                        break;
                if (time.time() - start) > timeout:
                    logger.error("Complete packet not received: " + data)
                    break
            except:
                raise;

        return packet;
        
    def run(self):
        try:
            logger.info("Connection from : " + self.ip + ":" + str(self.port))
            logger.info("Receiving module ID")
            self.socket.send("[GET /moduleId]")
            moduleIdReply = self.read();
            moduleIdReply = moduleIdReply.replace("[/moduleId/", "")
            self.moduleId = moduleIdReply.replace("]", "")
            
            logger.info("Receiving gpio0 state")
            self.socket.send("[GET /gpio0]")
            gpio0Reply = self.read();
            gpio0Reply = gpio0Reply.replace("[/gpio0/", "")
            self.gpio0State = gpio0Reply.replace("]", "")            
            config.updateSwitch(self.moduleId, "relay1", self.gpio0State)
             
            logger.info("Receiving gpio2 state")
            self.socket.send("[GET /gpio2]")
            gpio2Reply = self.read();
            gpio2Reply = gpio2Reply.replace("[/gpio2/", "")
            self.gpio2State = gpio2Reply.replace("]", "")
            config.updateSwitch(self.moduleId, "relay2", self.gpio0State)

            logger.info(config.getFormattedString())
            start = time.time()
            
            while True:
                if self.writeBuffer:
                    logger.info("Sending command: " + self.writeBuffer)
                    self.socket.send(self.writeBuffer)
                    status = self.read();
                    if (status == "[OK]"):
                        logger.info("State changed successfully")
                    else:
                        logger.error("Error changing state")

                #(readyRead, readyWrite, readyException) = select.select([self.socket], [], [], 5)
                #print readyRead
                #print readyWrite
                #print readyException
                
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
        logger.info(config.getFormattedString())

class Server(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.threadDict = dict()
        self.idCounter = 1
        self.dictLock = threading.Lock()
        
    def executeCommand(self, moduleId):
        #for key, value in self.threadDict.iteritems():
        print "test"

    def removeThread(self, id):
        self.dictLock.acquire();
        del self.threadDict[id];
        self.dictLock.release();
        
    def run(self):
    
        logger.info("Starting server on port: " + str(self.port))
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpsock.bind((self.host, self.port))
        tcpsock.listen(5)
        
        while True:
            logger.info("Listening for incoming connections...")
            (clientsock, (ip, port)) = tcpsock.accept()
            newthread = ClientThread(self, self.idCounter, ip, port, clientsock)
            newthread.start()
            self.dictLock.acquire()
            self.threadDict[self.idCounter] = newthread
            logger.info("Total connection:" + str(len(self.threadDict)) + "\n")
            self.dictLock.release()
            self.idCounter = self.idCounter + 1

        #for t in threads:
        #    t.join()

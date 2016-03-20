import socket
import threading
import select
import time
import json
import logger
import config

class APIServer(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port

    def isValidJson(self, jsonString):
        try:
            json_object = json.loads(jsonString)
        except ValueError, e:
            return False
        return True
        
    def read(self, clientsock, timeout = 10):
        packet = ""
        data = ""
        start = time.time()
        while True:
            try:
                delay = .5
                (readyRead, readyWrite, readyException) = select.select([clientsock], [], [], delay)
                if (readyRead):
                    data += clientsock.recv(2048)
                    if self.isValidJson(data):
                        packet = data
                        logger.info("Received packet : " + packet)
                        break;
                    #startIndex = data.find("[");
                    #endIndex = data.find("]");
                    #if (startIndex >= 0 and endIndex >= 0):
                    #    packet = data[startIndex:endIndex+1]
                    #    data = data[endIndex+1:]
                    #    logger.info("Received packet : " + packet)
                    #    break;
                if (time.time() - start) > timeout:
                    logger.error("Complete packet not received: " + data)
                    break
            except:
                raise;

        return packet;
        
    def run(self):    
        logger.info("Starting API server on port: " + str(self.port))
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpsock.bind((self.host, self.port))
        tcpsock.listen(5)
        
        while True:
            logger.info("Listening for incoming API call...")
            (clientsock, (ip, port)) = tcpsock.accept()
            command = self.read(clientsock);
            if (command):
                logger.info("API command: " + command)
                jsonCommand = json.loads(command)
                reply = ""
                if (jsonCommand['command'] == 'getStatus'):
                    reply = config.getString()

                logger.info("API reply: " + reply)
                clientsock.sendall(reply + "\r\n")
            else:
                logger.error("No command received")
            time.sleep(.5)
            clientsock.close()
            logger.info("Connection closed")
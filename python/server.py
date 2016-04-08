#!/usr/bin/env python

import time
import logger
import config
import server_socket
import api_server
import set_config

if __name__ == '__main__':
    logger.setupLogger();
    logger.info("========== SERVER STARTED ==========")

    # Dummy call to initialize the config object
    logger.info("Starting server with configuration:\n" + config.getFormattedString())

    logger.info("Staring Device Server")
    server = server_socket.Server(9000)
    server.daemon = True
    server.start()
    logger.info("Device Server started")

    logger.info("Staring API Server")
    api = api_server.APIServer(server, 9999)
    api.daemon = True
    api.start();
    #api_server.server = server
    #api_server.start()
    #api_server.start();
    logger.info("API server stopped")

    status = set_config.SetStatus();
    status.daemon = True
    status.start();
    
    while True:
        try:
            time.sleep(1)
        except:
            exit(0)

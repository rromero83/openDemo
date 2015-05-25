import logging
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
log = logging.getLogger('socketUdpReal')
log.setLevel(logging.ERROR)
log.addHandler(NullHandler())

import Log

import socket
import time

import socketUdp
import threading

class socketUdpReal(socketUdp.socketUdp):

    BUFSIZE = 1024
    
    def __init__(self,ipAddress,udpPort,callback):
        
        # log
        log.debug('creating instance')
        
        # initialize the parent class
        socketUdp.socketUdp.__init__(self,ipAddress,udpPort,callback)
        
        # change name
        self.name       = 'socketUdpRead@{0}:{1}'.format(self.ipAddress,self.udpPort)
        self.callback   = callback
        
        # local variables
        self.socketLock = threading.Lock()
        
        # open UDP port
        try:
            self.socket_handler  = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            self.socket_handler.bind((self.ipAddress,self.udpPort))
        except socket.error as err:
            log.critical(err)
            raise
        
        # start myself
        self.start()
    
    #======================== public ==========================================
    
    def sendUdp(self,destIp,destPort,msg):
        
        # convert msg to string
        msg = ''.join([chr(b) for b in msg])
        
        try:
        # send over UDP
            with self.socketLock:
                self.socket_handler.sendto(msg,(destIp,destPort))
        except:
            Log.writeError( " sendUdp socketUdpReal") #Modificat
            pass
        # increment stats
        self._incrementTx()
    
    def close(self):
        # declare that this thread has to stop
        self.goOn = False
        
        # send some dummy value into the socket to trigger a read
        self.socket_handler.sendto( 'stop', ('::1',self.udpPort) )
        
        # wait for this thread to exit
        self.join()
    
    #======================== private =========================================
    
    def run(self):
        while self.goOn:
            try:
                # blocking wait for something from UDP socket
                raw,conn = self.socket_handler.recvfrom(self.BUFSIZE)
            except socket.error as err:
                log.critical("socket error: {0}".format(err))
                self.goOn = False
                continue
            else:
                if not raw:
                    log.error("no data read from socket, stopping")
                    self.goOn = False
                    continue
                if not self.goOn:
                    log.warning("goOn is false")
                    continue
                
                timestamp = time.time()
                source    = (conn[0],conn[1])
                data      = [ord(b) for b in raw]
                
                log.debug("got {2} from {1} at {0}".format(timestamp,source,data))
                
                try:
                #call the callback with the params
                    self.callback(timestamp,source,data)
                except:
                    Log.writeError(" receive socketUdpReal") #Modificat
                    pass
        
        # if you get here, we are tearing down the socket
        
        # close the socket
        self.socket_handler.close()
        
        # log
        log.info("teardown")

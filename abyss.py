#!/usr/bin/env python3
import socketserver
import time
import threading
import random
import os

# **********************************************
#
# Python "netcat" Server CTF Challenge - ABYSS
# https://www.youtube.com/watch?v=kjDrGI8W-vg
#
# **********************************************

offset_min = 5
offset_max = 30

class Service(socketserver.BaseRequestHandler):
    def handle(self):
        # Handle connection
        print("Someone connected!")
        
        # Send the flag every minute or so
        offset = random.randint(offset_min, offset_max)
        start_time = int(time.time())

        while(True):
            if(int (time.time()) < start_time + offset):
                # This will send a bunch of random stuff from /dev/urandom        
                self.send(os.urandom(random.randint(10, 200)), newline = False)
                print(f"time: {time.time()},  waiting for: {start_time + offset}")
            else:                
                # if it is the special time, send the flag!
                flag = "USCGA{you_can_see_through_the_abyss}"
                self.send(flag, newline = False)
                print(f"flag: {flag}")

                # reset start time 
                start_time = int(time.time())
                offset = random.randint(offset_min, offset_max)

    def send(self, string, newline = True):
        # Add newline if needed
        if newline: 
            string = string + "\n"        
        
        # encode string to bytes
        if type(string) == type("string"):            
            string = string.encode()
        
        # Send request
        self.request.sendall(string)

    def receive(self, prompt = " > "):
        self.send(prompt, newline = False)
        return self.request.recv(4096).strip()

# This class required for threaded service
class ThreadedService(socketserver.ThreadingMixIn, socketserver.TCPServer, socketserver.DatagramRequestHandler):
    pass

def main():
    port = 6667
    # 0.0.0.0
    # A way to specify "any IPv4 address at all". It is used in this way when configuring servers (i.e. when binding listening sockets). This is known to TCP programmers as INADDR_ANY. (bind(2) binds to addresses, not interfaces.)
    # https://en.wikipedia.org/wiki/0.0.0.0
    host = '0.0.0.0'
    
    # OSError: [Errno 98] Address already in use
    # https://stackoverflow.com/questions/16433522/socketserver-getting-rid-of-errno-98-address-already-in-use
    # socketserver.TCPServer.allow_reuse_address = True

    server = ThreadedService((host, port), Service)    
    server.allow_reuse_address = True
    server_thread = threading.Thread(target = server.serve_forever)

    server_thread.daemon = True
    server_thread.start()

    print("Server started on port", port)
    while (True): time.sleep(60)

if __name__ == "__main__":
    main()
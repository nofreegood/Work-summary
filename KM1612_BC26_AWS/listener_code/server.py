
import threading
import socket
from base64 import b64encode
from helper import ConfigHelper
from httpclient import HttpClient

class Reader(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
    def run(self):
        while True:
            IDlength = self.client.recv(1)
            if(IDlength):
                lenth1 = int(IDlength[0])
                ID = self.client.recv(lenth1)
                Taglength = self.client.recv(1)
                if(Taglength):
                    lenth2 = int(Taglength[0])
                    Tagdata = self.client.recv(lenth2)
                    Datalength = self.client.recv(1)
                    if(Datalength):
                        lenth3 = int(Datalength[0])
                        Data = self.client.recv(lenth3)
            if(IDlength):
                IDstring = b64encode(ID).decode()
                print(IDstring+'\n')
                Tagstring = str(Tagdata[0])
                print(Tagstring+'\n')
                Datastring = b64encode(Data).decode()
                print(Datastring+'\n')
                config = ConfigHelper('config.yaml')
                client = HttpClient(*config.api)
                public_id = IDstring
                tag = int(Tagstring)
                data = Datastring
                client.main_entry(public_id,tag,data, *config.reference_llh)

            else:
                break
        ip = self.client.getpeername()
        print('start data transform:\n',ip)
        n = bytes[0x34,0x12]
        self.clent.send(n,ip)
        print("close:", self.client.getpeername())
class Listener(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(0)
    def run(self):
        print("listener started")
        while True:
            client, cltadd = self.sock.accept()
            Reader(client).start()
            cltadd = cltadd
            print("accept a connect")
lst  = Listener(49962) 
lst.start() 

 

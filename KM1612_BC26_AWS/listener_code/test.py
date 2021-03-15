
import time
import threading
import socket
from base64 import b64encode
from base64 import b64decode
from helper import ConfigHelper
from httpclient import HttpClient
from struct import pack 
from serial_util import * 

class Reader(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
    def run(self):
        while True:
            config = ConfigHelper('config.yaml')
            cmdtype = self.client.recv(1)
            if(cmdtype):
                if(cmdtype[0] == 0x08):#0x08代表接受原始数据并上传服务器
                    n = cmdtype[0]
                    lenth1 = int(n)
                    ID = self.client.recv(lenth1)
                    Taglength = self.client.recv(1)
                    if(Taglength):
                        Datalength = self.client.recv(1)
                        if(Datalength):
                            lenth3 = int(Datalength[0])
                            Data = self.client.recv(lenth3)
                    IDstring = b64encode(ID).decode()
                    print(IDstring+'\n')
                    Tagstring = str(Taglength[0])
                    print(Tagstring+'\n')
                    Datastring = b64encode(Data).decode()
                    print(Datastring+'\n') 
                    client2 = HttpClient(*config.api)
                    public_id = IDstring
                    tag = int(Tagstring)
                    client2.main_entry(public_id,tag,Datastring, *config.reference_llh)       
                elif(cmdtype[0] == 0x09):#0x09代表请求GET_POINT信息
                    ip = self.client.getpeername()
                    print('start data transform:\n',ip)
                    preamble = bytes([0xC9,0x1E,0xB1,0x81])
                    t = int(time.time())
                    num_points = config.num_points
                    p=pack('<II', num_points, t)
                    header = SerialHeader(9, len(p))
                    reply = SerialCommand(header, p)
                    print(reply.bytes)
                    self.client.send(reply.bytes)
                    print('\n over')
                elif(cmdtype[0] == 0x07):#0X07代表请求初始化信息
                    idlength = self.client.recv(1)
                    length = int(idlength[0])
                    ID = self.client.recv(length)
                    IDstring = b64encode(ID).decode()
                    print(type(IDstring))
                    public_id = IDstring
                    print(IDstring+'\n')
                    tag = 7
                    data = str()
                    
                    client2 = HttpClient(*config.api)
                    resp = client2.main_entry(public_id,tag,data, *config.reference_llh)
                    pd_b64 = resp and resp.get('data')
                    prediction = pd_b64 and b64decode(pd_b64)
                    header = SerialHeader(8, len(prediction))
                    reply = SerialCommand(header, prediction)
                    self.client.send(reply.bytes)
                    print(reply.bytes)
                    
                    

                else:
                    break
            else:
                break
            
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

 






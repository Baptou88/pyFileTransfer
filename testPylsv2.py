import pyLSV2
from pyLSV2 import LSV2StateException

import socket
import logging
import sys 
import os

host_machine = 'localhost'
try:
    con = pyLSV2.LSV2(
        hostname=host_machine, 
        port=19000, 
        timeout=10
        
        )
    
    con.connect()
    if(con.login(login=pyLSV2.Login.DNC,password="807667")):
        print("login success")
    else:
        print("login error ")
    files = con.get_file_list(path="TNC:/EM/")
    for file in files:
        print(file)
        
    # local_path = "C:/Users/Baptou88/Documents/Programmation/pyFileTransfer/test/bqtou.h"
    # if os.path.exists(local_path):
    #     print("folder exist")
    #     print(os.path.abspath(local_path))
    # success = con.recive_file(remote_path="TNC:/EM/bqptou.h",local_path=os.path.abspath(local_path),override_file=True)
    # pos = con.axes_location()
    source_path = "C:/Users/Baptou88/Documents/Programmation/pyFileTransfer/test/test.h"
    dest_path = "TNC:/EM/"
    print(con.execution_state())
    success = con.send_file(local_path=os.path.abspath(source_path), remote_path=dest_path, override_file=True,binary_mode=False)
    if(success):
        print("ok")
    else:
        print("error transfer")
except socket.gaierror as ex:
    print("An Exception occurred: '%s'", ex)
    print("Could not resove host information: '%s'", host_machine)
    sys.exit(-2)
except  LSV2StateException as e:
    print(e)
#except :
    #print("par là")
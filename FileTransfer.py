from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from plyer import notification
import pyLSV2
import os
import argparse
import logging

dest_path =  "TNC:/EM/"
path = "test/"  # Remplacez ceci par le chemin du dossier que vous souhaitez surveiller.


class MyHandler(FileSystemEventHandler):
    
    def on_modified(self, event):
       
        if event.is_directory:
            return
        
        print(f'File {event.src_path} has been modified.')
        success = con.send_file(local_path=os.path.abspath(event.src_path), remote_path=dest_path, override_file=True,binary_mode=False)
        
        title = "Modified"
        message = f'File {event.src_path} has been modified. '+ f' {success} '
        notification.notify(
            title= title,
            message= message,
            app_name= "Python",
            timeout=5
        )

    def on_created(self, event):
        if event.is_directory:
            return
        if args.new == False:
            return

        success = con.send_file(local_path=os.path.abspath(event.src_path), remote_path=dest_path, override_file=True,binary_mode=False)

        title = "Created"
        message = f'File {event.src_path} has been created.'
        notification.notify(
            title= title,
            message= message + f' {success} '  ,
            app_name= "Python",
            timeout=5
        )

    def on_deleted(self, event):
        if event.is_directory:
            return
        if args.delete == False:
            return
        nom_du_fichier = os.path.basename(event.src_path)
        emplacement = f'{dest_path}{nom_du_fichier}'

        if not con.file_info(emplacement) == None:
            status = con.delete_file(emplacement)
            title = "Created"
            message = f'File {event.src_path} has been deleted.'
            notification.notify(
                title= title,
                message= message + f' {status} '  ,
                app_name= "Python",
                timeout=5
            )
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transfert de fichier Automatic pour Heidenhain")

    parser.add_argument(
        "-d",
        "--debug",
        help="Print lots of debugging statements",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Be verbose",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    parser.add_argument("--address", help="ip or hostname of control", type=str, default="localhost")
    
    parser.add_argument("--new", help="send on new file", type=bool, default=True)
    parser.add_argument("--delete", help="remove on delete file", type=bool, default=True)
    args = parser.parse_args()
    
    logging.basicConfig(level=args.loglevel)
    
    host_machine = args.address

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        con = pyLSV2.LSV2(
        hostname=host_machine, 
        port=19000, 
        timeout=30,
        safe_mode=False
        
        )
    
        con.connect()
        if(con.login(login=pyLSV2.Login.FILETRANSFER)):
            print("login success")
        else:
            print("login error ")

        print(con.versions.control)
        print(con.versions.nc_sw)

        while True:
            
            time.sleep(1000)
            pass
    except KeyboardInterrupt:
        observer.stop()
        con.disconnect()
        exit(0)
    except ConnectionRefusedError as e:
        print(e)
        exit(0)

    observer.join()

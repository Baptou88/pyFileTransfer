from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from plyer import notification
import pyLSV2
import os
import argparse

dest_path =  "TNC:/EM/"
path = "test/"  # Remplacez ceci par le chemin du dossier que vous souhaitez surveiller.


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(event.event_type)
        print(event.is_synthetic)
        if event.is_directory:
            return
        # print(f'File {event.src_path} has been modified.')
        # title = "Modified"
        # message = f'File {event.src_path} has been modified.'
        # notification.notify(
        #     title= title,
        #     message= message,
        #     app_name= "zer",
        #     timeout=5
        # )

    def on_created(self, event):
        if event.is_directory:
            return
        print(f'File {event.src_path} has been created.')
        success = con.send_file(local_path=os.path.abspath(event.src_path), remote_path=dest_path, override_file=True,binary_mode=False)

        title = "Created"
        message = f'File {event.src_path} has been created.'
        notification.notify(
            title= title,
            message= message + f' {success} '  ,
            app_name= "zer",
            timeout=5
        )

    def on_deleted(self, event):
        if event.is_directory:
            return
        print("deleted")
        nom_du_fichier = os.path.basename(event.src_path)
        print(f'Fichier à supprimer: {nom_du_fichier}')
        emplacement = f'{dest_path}{nom_du_fichier}'
        print(f'Fichier à supprimer: {emplacement}')
        if not con.file_info(emplacement) == None:
            status = con.delete_file(emplacement)
            print(f'supppression {status}')
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transfert de fichier Automatic pour Heidenhain")

    # parser.add_argument("address", nargs="?", default="192.168.56.101", type=str)

    parser.add_argument("--address", help="ip or hostname of control", type=str, default="localhost")
    args = parser.parse_args()
    print(args.address)
    host_machine = args.address
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        con = pyLSV2.LSV2(
        hostname=host_machine, 
        port=19000, 
        timeout=30
        
        )
    
        con.connect()
        if(con.login(login=pyLSV2.Login.FILETRANSFER)):
            print("login success")
        else:
            print("login error ")


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

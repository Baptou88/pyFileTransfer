from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from plyer import notification

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(event.event_type)
        print(event.is_synthetic)
        if event.is_directory:
            return
        print(f'File {event.src_path} has been modified.')
        title = "Modified"
        message = f'File {event.src_path} has been modified.'
        notification.notify(
            title= title,
            message= message,
            app_name= "zer",
            timeout=5
        )
        
    def on_created(self, event):
        if event.is_directory:
            return
        print(f'File {event.src_path} has been created.')
        title = "Created"
        message = f'File {event.src_path} has been created.'
        notification.notify(
            title= title,
            message= message,
            app_name= "zer",
            timeout=5
        )

    def on_deleted(self, event):
        if event.is_directory:
            return
        print("deleted")

if __name__ == "__main__":
    path = "test/"  # Remplacez ceci par le chemin du dossier que vous souhaitez surveiller.

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            
            time.sleep(1000)
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

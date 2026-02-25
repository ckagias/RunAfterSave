import time
import subprocess
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LiveRunHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None

    def on_modified(self, event):
        # Ignore directories and non-Python files
        if event.is_directory or not event.src_path.endswith('.py'):
            return
        
        # Prevent the script from running itself
        filename = os.path.basename(event.src_path)
        if filename == 'runlive.py':
            return

        print(f"\nDetected change in {filename}.")
        
        # Terminate the previous run if it's still going
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

        # Run the updated file
        self.process = subprocess.Popen([sys.executable, event.src_path])

if __name__ == "__main__":
    path = "." # Watches the current directory
    event_handler = LiveRunHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    
    print(f"Watching for changes in Python files. Press Ctrl+C to stop.")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.terminate()
        print("\n[runlive] Stopped.")
        
    observer.join()
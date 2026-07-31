import shutil
import time
from sys import argv
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Extensions and their target directories
dirs = {   
    # Images
    "jpeg": "Images", "png": "Images", "jpg": "Images", "tiff": "Images", "gif": "Images",
    # Videos
    "mp4": "Videos", "mkv": "Videos", "mov": "Videos", "webm": "Videos", "flv": "Videos",
    # Music
    "mp3": "Music", "ogg": "Music", "wav": "Music", "flac": "Music",
    # Program Files
    "py": "Program Files", "js": "Program Files", "cpp": "Program Files",
    "html": "Program Files", "css": "Program Files", "c": "Program Files", "sh": "Program Files",
    # Documents
    "pdf": "Documents", "doc": "Documents", "docx": "Documents",
    "txt": "Documents", "ppt": "Documents", "ods": "Documents", "csv": "Documents"
}

def get_dir(filename):
    extension = filename.suffix.lstrip('.').lower()
    return dirs.get(extension, "Miscellaneous")

# --- NEW EVENT HANDLER CLASS ---
TEMP_EXTS = {".crdownload", ".part", ".tmp", ".download"}

class DownloadHandler(FileSystemEventHandler):
    def process_file(self, file_path):
        filename = Path(file_path)

        if not filename.is_file() or filename.suffix.lower() in TEMP_EXTS:
            return

        time.sleep(1)  # Brief pause for browser file lock release

        try:
            destination_dir = filename.parent / get_dir(filename)
            destination_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(filename), str(destination_dir / filename.name))
            print(f"[+] Organized: {filename.name} -> {get_dir(filename)}/")
        except Exception as e:
            print(f"[-] Could not move {filename.name}: {e}")

    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(event.dest_path)

# --- START WATCHER ENGINE ---
if __name__ == "__main__":
    target_path = Path(argv[1]).expanduser().resolve() if len(argv) == 2 else Path("~/Downloads").expanduser().resolve()

    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, str(target_path), recursive=False)

    print(f"[*] Watching for downloads in: {target_path}")
    print("[*] Press Ctrl+C to stop.")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
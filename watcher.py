import os
import sys
import time
from pathlib import Path
from rag_ingest import DocumentIngestionEngine, calculate_file_hash, SUPPORTED_EXTENSIONS

WATCH_DIR = os.getenv("LUNARIS_WATCH_DIR", os.path.join(os.path.dirname(__file__), "documents"))
POLL_INTERVAL_SECONDS = int(os.getenv("WATCHER_POLL_INTERVAL", "5"))

class LunarisFolderWatcher:
    """
    Continuous background watcher for Lunaris AI documents.
    Detects additions, modifications, and deletions in real-time and updates pgvector.
    """
    def __init__(self, watch_dir: str = WATCH_DIR):
        self.watch_dir = Path(watch_dir)
        self.engine = DocumentIngestionEngine()
        self.known_files = {} # {file_path: file_hash}
        self.is_running = False

    def scan_and_sync(self):
        """Single pass to detect new, modified, or deleted files."""
        if not self.watch_dir.exists():
            self.watch_dir.mkdir(parents=True, exist_ok=True)
            print(f"[Watcher] Created watching folder: {self.watch_dir.resolve()}")

        current_files = {}
        for file_path in self.watch_dir.glob("**/*"):
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                try:
                    f_hash = calculate_file_hash(str(file_path))
                    current_files[str(file_path.resolve())] = (f_hash, file_path)
                except Exception as e:
                    print(f"[Watcher Error] Reading {file_path.name}: {e}")

        # Check for added or modified files
        for f_path, (f_hash, path_obj) in current_files.items():
            if f_path not in self.known_files:
                print(f"[Watcher] Detected NEW file: {path_obj.name}")
                res = self.engine.ingest_file(str(path_obj), title=path_obj.stem)
                print(f"[Watcher] Ingestion: {res.get('status')} - {res.get('message', f'Indexed {res.get(\"chunks_indexed\")} chunks')}")
                self.known_files[f_path] = f_hash
            elif self.known_files[f_path] != f_hash:
                print(f"[Watcher] Detected MODIFIED file: {path_obj.name}")
                res = self.engine.ingest_file(str(path_obj), title=path_obj.stem, force_reindex=True)
                print(f"[Watcher] Re-indexed: {res.get('status')} - {res.get('chunks_indexed', 0)} chunks")
                self.known_files[f_path] = f_hash

        # Check for deleted files
        deleted_paths = [p for p in self.known_files if p not in current_files]
        for d_path in deleted_paths:
            print(f"[Watcher] Detected DELETED file: {Path(d_path).name}")
            deleted_chunks = self.engine.delete_document_by_path_or_title(d_path)
            print(f"[Watcher] Purged {deleted_chunks} obsolete vector chunks from pgvector.")
            del self.known_files[d_path]

    def start(self):
        """Starts the watcher loop."""
        self.is_running = True
        print(f"==================================================")
        print(f"👁️  Lunaris AI Document Watcher Active")
        print(f"📁 Monitoring Folder: {self.watch_dir.resolve()}")
        print(f"⏱️  Poll Interval: {POLL_INTERVAL_SECONDS}s")
        print(f"==================================================")

        # Initial baseline sync
        self.scan_and_sync()

        try:
            while self.is_running:
                time.sleep(POLL_INTERVAL_SECONDS)
                self.scan_and_sync()
        except KeyboardInterrupt:
            print("\n[Watcher] Gracefully stopping document watcher.")
            self.is_running = False

if __name__ == "__main__":
    watcher = LunarisFolderWatcher()
    watcher.start()

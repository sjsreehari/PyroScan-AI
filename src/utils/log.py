import os
import json
from datetime import datetime

class Logger:
    LOG_FILE_PATH = os.path.join("db", "log_file.ndjson")

    def __init__(self):
        os.makedirs(os.path.dirname(self.LOG_FILE_PATH), exist_ok=True)

    def _write_log(self, level: str, message: str, attack_id: str):
        timestamp = datetime.now().strftime("%d/%m/%y - %H:%M:%S")
        log_entry = {
            "attack_id": attack_id,
            "timestamp": timestamp,
            "level": level.upper(),
            "message": message
        }

        with open(self.LOG_FILE_PATH, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def info(self, message: str, attack_id):
        self._write_log("info", message, attack_id )

    def warn(self, message: str, attack_id):
        self._write_log("warn", message, attack_id)

    def error(self, message: str, attack_id):
        self._write_log("error", message, attack_id)

    def success(self, message: str, attack_id):
        self._write_log("success", message, attack_id)


logger = Logger()

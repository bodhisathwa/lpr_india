import sqlite3
import csv
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = 'database/parking_logs.db'):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Initialize database with proper schema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        plate TEXT NOT NULL,
                        status TEXT NOT NULL,
                        source TEXT NOT NULL,
                        timestamp DATETIME NOT NULL,
                        processing_time REAL NOT NULL
                    )
                ''')
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_plate_timestamp 
                    ON logs (plate, timestamp)
                ''')
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            raise

    def log_entry(self, plate: str, status: str, source: str, processing_time: float):
        """Securely log plate recognition result"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO logs 
                    (plate, status, source, timestamp, processing_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (plate, status, source, datetime.now(), processing_time))
        except Exception as e:
            logger.error(f"Failed to log entry: {str(e)}")

    def get_recent_logs(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent logs with type safety"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('''
                    SELECT plate, status, source, timestamp, processing_time
                    FROM logs
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to fetch logs: {str(e)}")
            return []

class BlocklistManager:
    def __init__(self, csv_path: str = 'database/blocked_plates.csv'):
        self.csv_path = csv_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create empty blocklist file if not exists"""
        try:
            open(self.csv_path, 'a').close()
        except IOError as e:
            logger.error(f"Blocklist file error: {str(e)}")

    def check_blocked(self, plate: str) -> bool:
        """Case-insensitive blocklist check"""
        try:
            with open(self.csv_path, 'r') as f:
                reader = csv.reader(f)
                return any(plate.strip().upper() in row[0].upper() for row in reader if row)
        except Exception as e:
            logger.error(f"Blocklist check failed: {str(e)}")
            return False

    def get_blocked_count(self) -> int:
        """Count blocked plates"""
        try:
            with open(self.csv_path, 'r') as f:
                return sum(1 for _ in f)
        except Exception as e:
            logger.error(f"Blocklist count failed: {str(e)}")
            return 0
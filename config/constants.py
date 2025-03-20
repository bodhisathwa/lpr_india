# config/constants.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'parking_logs.db')
BLOCKLIST_PATH = os.path.join(BASE_DIR, 'database', 'blocked_plates.csv')
SAMPLE_IMAGE_DIR = os.path.join(BASE_DIR, 'assets', 'demo_plates')
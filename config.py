"""Configuration for OFAC screening app."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OFAC_DB_FOLDER = os.path.join(BASE_DIR, "OFAC DB")
DATABASE_PATH = os.path.join(BASE_DIR, "ofac_screening.db")

# Fuzzy match: minimum score 0-100 (higher = stricter)
FUZZY_THRESHOLD = 60
# Max number of matches to return
MAX_MATCHES = 100

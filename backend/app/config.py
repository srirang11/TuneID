import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "fingerprints.db")


SR = 11025
N_FFT = 2048
HOP = 512

PEAK_NEIGHBORHOOD = (20, 20)
MIN_AMPLITUDE = 10

TARGET_ZONE_START = 1
TARGET_ZONE_WIDTH = 10
FAN_VALUE = 15

MIN_MATCHES = 10

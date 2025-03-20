import re

# Official Indian state/UT codes (e.g., DL, MH, KA, PY, etc.)
STATE_CODES = [
    "AP", "AR", "AS", "BR", "CG", "CH", "DD", "DL", "DN", "GA", "GJ", "HP", 
    "HR", "JH", "JK", "KA", "KL", "LA", "LD", "MH", "ML", "MN", "MP", "MZ", 
    "NL", "OD", "PB", "PY", "RJ", "SK", "TN", "TR", "TS", "UK", "UP", "WB", "AN"
]

# Regex patterns for all states
PLATE_PATTERNS = {
    # Private Vehicles (DL-01-AB-1234, KA-51-P-9999)
    "PRIVATE": re.compile(
        r"^(" + "|".join(STATE_CODES) + r")"  # State code validation
        r"\d{1,2}"  # District number (1-2 digits)
        r"[A-Z]{1,3}"  # Alphabetic series (1-3 letters)
        r"\d{4}$"  # Unique number (4 digits)
    ),
    
    # Commercial Vehicles (TN-38-N-1234, GJ-01-T-4532)
    "COMMERCIAL": re.compile(
        r"^(" + "|".join(STATE_CODES) + r")"
        r"\d{2}"  # District number (2 digits)
        r"[A-Z]{1}"  # Vehicle type (e.g., T, C, S)
        r"\d{4}$"
    ),
    
    # Bharat Series (29-BH-2345-AA)
    "BHARAT": re.compile(r"^\d{2}BH\d{4}[A-Z]{2}$"),
    
    # Diplomatic Vehicles (CD 123 XYZ)
    "DIPLOMATIC": re.compile(r"^CD\d{1,3}[A-Z]{1,3}$"),
}
import re
from typing import Optional, List

class PlateValidator:
    def __init__(self):
        self.STATE_CODES = [
            "AP", "AR", "AS", "BR", "CG", "CH", "DD", "DL", "DN", "GA", "GJ", "HP",
            "HR", "JH", "JK", "KA", "KL", "LA", "LD", "MH", "ML", "MN", "MP", "MZ",
            "NL", "OD", "PB", "PY", "RJ", "SK", "TN", "TR", "TS", "UK", "UP", "WB",
            "AN", "BH"
        ]
        self.OCR_SUBSTITUTIONS = str.maketrans('OIlZSB', '011258')
        self.PATTERNS = {
            'private': re.compile(
                r'^(' + '|'.join(self.STATE_CODES) + r')[\s.-]?(\d{1,2})[\s.-]?([A-Z]{1,3})[\s.-]?(\d{1,4})$',
                re.IGNORECASE
            ),
            'commercial': re.compile(
                r'^(' + '|'.join(self.STATE_CODES) + r')[\s.-]?(\d{2})[\s.-]?([A-Z])[\s.-]?(\d{4})$',
                re.IGNORECASE
            ),
            'bharat': re.compile(
                r'^(\d{2})[\s.-]?BH[\s.-]?(\d{4})[\s.-]?([A-Z]{2})$',
                re.IGNORECASE
            )
        }

    def validate_plate(self, ocr_results: List[str]) -> Optional[str]:
        """Validate and format license plate"""
        for text in self._preprocess_text(ocr_results):
            for pattern_name, pattern in self.PATTERNS.items():
                match = pattern.match(text)
                if match:
                    return self._format_plate(match.groups(), pattern_name)
        return None

    def _preprocess_text(self, texts: List[str]) -> List[str]:
        """Clean and prioritize OCR results"""
        processed = [
            t.translate(self.OCR_SUBSTITUTIONS)
            .upper()
            .replace(" ", "")
            .replace(".", "")
            .replace("-", "")
            for t in texts
        ]
        return sorted(processed, key=lambda x: (-len(x), x))

    def _format_plate(self, groups: tuple, plate_type: str) -> str:
        """Standardize plate formatting"""
        if plate_type == 'private':
            return f"{groups[0]}-{groups[1]}-{groups[2]}-{groups[3]}"
        elif plate_type == 'commercial':
            return f"{groups[0]}-{groups[1]}-{groups[2]}-{groups[3]}"
        elif plate_type == 'bharat':
            return f"{groups[0]}-BH-{groups[1]}-{groups[2]}"
        return ''.join(groups)
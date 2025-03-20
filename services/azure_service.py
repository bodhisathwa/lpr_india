import os
import time
import logging
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv
from typing import List
load_dotenv()
logger = logging.getLogger(__name__)

class AzureOCR:
    def __init__(self):
        self.client = ComputerVisionClient(
            os.getenv("AZURE_ENDPOINT"),
            CognitiveServicesCredentials(os.getenv("AZURE_API_KEY"))
        )
        self.timeout = 30
        self.max_retries = 3

    def extract_text(self, image_path: str) -> List[str]:
        """Robust text extraction with retry logic."""
        for attempt in range(self.max_retries):
            try:
                with open(image_path, "rb") as image_stream:
                    operation = self.client.read_in_stream(image_stream, raw=True)
                    return self._poll_for_results(operation)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"OCR failed after {self.max_retries} attempts: {str(e)}")
                    raise
                time.sleep(1)
        return []

    def _poll_for_results(self, operation) -> List[str]:
        """Handle OCR operation polling with timeout."""
        operation_id = operation.headers["Operation-Location"].split("/")[-1]
        start_time = time.time()
        
        while True:
            result = self.client.get_read_result(operation_id)
            if result.status == OperationStatusCodes.succeeded:
                return self._parse_results(result)
            if result.status == OperationStatusCodes.failed:
                logger.error("Azure OCR processing failed")
                return []
            if time.time() - start_time > self.timeout:
                logger.warning("OCR processing timeout")
                return []
            time.sleep(1)

    def _parse_results(self, result) -> List[str]:
        """Extract and prioritize potential plate numbers."""
        from typing import List
        texts = []
        for page in result.analyze_result.read_results:
            for line in page.lines:
                clean_text = line.text.strip().replace(" ", "").upper()
                if 8 <= len(clean_text) <= 15 and any(c.isdigit() for c in clean_text):
                    texts.insert(0, clean_text)  # Prioritize likely plates
                else:
                    texts.append(clean_text)
        return texts
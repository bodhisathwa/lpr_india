import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self, max_dimension=800):
        self.max_dimension = max_dimension

    def preprocess(self, image_path: str) -> str:
        """Enhanced preprocessing pipeline"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Invalid image file")
            
            img = self._resize_image(img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            blurred = cv2.bilateralFilter(enhanced, 9, 75, 75)
            processed = self._adaptive_threshold(blurred)
            
            output_path = "temp/processed.jpg"
            cv2.imwrite(output_path, processed)
            return output_path
        except Exception as e:
            logger.error(f"Image processing failed: {str(e)}")
            raise

    def _resize_image(self, img: np.ndarray) -> np.ndarray:
        """Maintain aspect ratio while resizing"""
        h, w = img.shape[:2]
        if max(h, w) > self.max_dimension:
            ratio = self.max_dimension / max(h, w)
            return cv2.resize(img, (0,0), fx=ratio, fy=ratio)
        return img

    def _adaptive_threshold(self, img: np.ndarray) -> np.ndarray:
        """Optimized thresholding for plate detection"""
        return cv2.adaptiveThreshold(
            img, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
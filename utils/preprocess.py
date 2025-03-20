import cv2
import numpy as np

def preprocess_image(image_path: str) -> str:
    """Advanced plate localization and preprocessing"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Invalid image file")
    
    # Convert to grayscale and enhance contrast
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Bilateral filtering and edge detection
    blurred = cv2.bilateralFilter(enhanced, 11, 75, 75)
    edges = cv2.Canny(blurred, 30, 200)
    
    # Find contours with plate-like aspect ratios
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    plate = None
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        if 2.5 < aspect_ratio < 5.0:  # Typical plate aspect ratios
            plate = img[y:y+h, x:x+w]
            break
    
    # Fallback to full image if no plate found
    if plate is None:
        plate = enhanced
    
    # Final processing
    plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY) if plate.ndim ==3 else plate
    _, thresh = cv2.threshold(plate_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Save processed image
    output_path = "temp/processed.jpg"
    cv2.imwrite(output_path, thresh)
    return output_path
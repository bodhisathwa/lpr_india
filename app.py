import streamlit as st
import time
import cv2
import numpy as np
from datetime import datetime
from services.azure_service import AzureOCR
from services.database_service import DatabaseManager, BlocklistManager
from services.image_service import ImageProcessor
from utils.validators import PlateValidator
from dotenv import load_dotenv

load_dotenv()

# Initialize components
ocr = AzureOCR()
validator = PlateValidator()
db = DatabaseManager()
blocklist = BlocklistManager()
image_processor = ImageProcessor(max_dimension=800)

# Configure UI
st.set_page_config(
    page_title="LPR System - India",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🚗 Real-Time Indian License Plate Recognition (LPR) System")
   
    
    # Input source selection
    input_source = st.radio(
        "Select Input Source:",
        ["File Upload", "External Camera"],
        horizontal=True
    )
    
    if input_source == "File Upload":
        handle_file_upload()
    else:
        handle_external_camera()
    
    display_sidebar_info()

def handle_file_upload():
    uploaded = st.file_uploader("Upload Vehicle Image", type=["jpg", "png", "jpeg"])
    if uploaded:
        process_image(uploaded.read(), "UPLOAD")

def handle_external_camera():
    st.markdown("### External Camera Setup")
    cam_index = st.number_input("Camera Index", min_value=0, max_value=4, value=0)
    
    if st.button("Start Capture"):
        cap = cv2.VideoCapture(cam_index)
        frame_window = st.image([])
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture video")
                break
            
            # Resize and display frame
            frame = cv2.resize(frame, (640, 480))
            frame_window.image(frame, channels="BGR")
            
            if st.button("Stop Capture"):
                cap.release()
                break

def process_image(image_data: bytes, source: str):
    """Core processing pipeline"""
    try:
        # Save input image
        input_path = "temp/input.jpg"
        with open(input_path, "wb") as f:
            f.write(image_data)
        
        # Process image
        start_time = time.time()
        processed_path = image_processor.preprocess(input_path)
        ocr_results = ocr.extract_text(processed_path)
        plate = validator.validate_plate(ocr_results)
        proc_time = time.time() - start_time
        
        # Display results
        with st.expander("Processing Details", expanded=True):
            col1, col2 = st.columns(2)
            col1.image(input_path, caption="Original Image")
            col2.image(processed_path, caption="Processed Image")
        
        if plate:
            handle_valid_plate(plate, proc_time, source)
        else:
            handle_invalid_plate(ocr_results)

    except Exception as e:
        st.error(f"Processing Error: {str(e)}")

def handle_valid_plate(plate: str, proc_time: float, source: str):
    """Handle successful plate recognition"""
    is_blocked = blocklist.check_blocked(plate)
    status = "BLOCKED" if is_blocked else "ALLOWED"
    db.log_entry(plate, status, source, proc_time)
    
    st.success(f"**Valid License Plate:** `{plate}`")
    st.metric("Processing Time", f"{proc_time:.2f}s")
    
    if is_blocked:
        st.error("## 🚨 Security Alert: Blocked Vehicle Detected")
        st.audio("assets/alert.mp3")
    else:
        st.success("## ✅ Vehicle Authorized: Access Granted")

def handle_invalid_plate(ocr_results):
    """Handle unrecognized plates"""
    st.warning("No Valid Indian License Plate Detected")
    with st.expander("OCR Debug Information"):
        st.write("Raw OCR Results:", ocr_results)
        st.write("Possible Issues:")
        st.markdown("- Low image quality")
        st.markdown("- Non-standard plate format")
        st.markdown("- Obstructions in plate area")

def display_sidebar_info():
    """Show project information and system status"""
    st.sidebar.title("About the Project")
    st.sidebar.markdown("""
    This is a **Real-Time Indian License Plate Recognition (LPR) System** that uses **Azure Computer Vision for OCR** and **custom validation logic** to accurately detect and validate Indian license plates. The system handles various plate formats, including private, commercial, Bharat series, and diplomatic plates.
    """)
    st.sidebar.markdown("### Key Features:")
    st.sidebar.markdown("""
    - **OCR Extraction**: Uses Azure Computer Vision to extract text from license plate images.
    - **Validation Logic**: Validates Indian license plate formats using regex patterns.
    - **Image Preprocessing**: Enhances plate region before OCR using advanced image processing techniques.
    - **User Interface**: Built using Streamlit for a user-friendly interface.
    - **Database Integration**: Logs all recognized plates with timestamps and processing times.
    """)
    st.sidebar.markdown("### How to Use:")
    st.sidebar.markdown("""
    1. Upload an image or use an external camera to capture a license plate.
    2. The system will preprocess the image, extract text, and validate the license plate.
    3. Results will be displayed in real-time.
    """)
    
    # Footer (unchanged)
st.markdown("---")
st.markdown("Developed with ❤️ by Bodhi Sathwa:)")


if __name__ == "__main__":
    main()
import streamlit as st
import os
from services.azure_service import AzureOCR
from dotenv import load_dotenv

load_dotenv()

def main():
    st.title("Azure OCR Tester")
    
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        # Save temporary file
        temp_path = "temp/test_image.jpg"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Display image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        # Process OCR
        try:
            ocr = AzureOCR()
            results = ocr.extract_text(temp_path)
            
            if results:
                st.success("OCR Results:")
                st.write(results)
            else:
                st.error("No text detected")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
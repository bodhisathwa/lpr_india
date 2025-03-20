# Indian License Plate Recognition System

## Overview
A system designed to recognize and validate Indian vehicle license plates using Azure Computer Vision OCR technology. This project processes images to extract license plate text and validates them against Indian license plate formats.

## Prerequisites
- Python 3.8 or newer
- Visual Studio Code
- Azure account with Computer Vision API subscription
- Internet connection

## Installation Guide

### Step 1: Download the Project
1. Download the ZIP file from GitHub
2. Extract to a location of your choice
3. Remember the path where you extracted it

### Step 2: Open in Visual Studio Code
1. Launch VS Code
2. Select **File → Open Folder**
3. Navigate to the extracted project folder
4. Click **Select Folder**

### Step 3: Set Up Python Environment
# Open VS Code terminal (Terminal → New Terminal)

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Create necessary folders
mkdir temp
mkdir database

### Step 4: Azure API Configuration
1. Create a file named `.env` in the project root folder
2. Add your Azure credentials:
   AZURE_API_KEY=your_azure_key_here
   AZURE_ENDPOINT=your_azure_endpoint_here

3. To get Azure credentials:
   - Log in to Azure Portal (https://portal.azure.com)
   - Navigate to your Computer Vision resource
   - Find **Keys and Endpoint** in the left menu
   - Copy Key 1 and the Endpoint URL

### Step 5: Running the Application
# Make sure your virtual environment is activated
# Then run:
streamlit run app.py

The application will open in your default web browser (typically at http://localhost:8501)

## Using the Application
1. Upload a license plate image using the file uploader
2. View the extracted text and validation results
3. The system will store results in the database for future reference

## Troubleshooting Common Issues

Problem: Azure OCR not working
Solution: Verify your API key and endpoint in the .env file

Problem: Missing Python modules
Solution: Run pip install -r requirements.txt again

Problem: Image not recognized
Solution: Ensure the image is clear and well-lit

Problem: Azure module error
Solution: Run pip install azure-cognitiveservices-vision-computervision

Problem: Streamlit not found
Solution: Run pip install streamlit

## Project Structure
indian-lpr/
├── app.py                # Main application
├── services/             # Core functionality
├── utils/                # Helper functions
├── config/               # Configuration files
├── temp/                 # Temporary image storage
├── database/             # Stores recognition history
├── requirements.txt      # Package dependencies
└── README.md             # This file

## License
[MIT License or your preferred license]

# Setting up the Indian License Plate Recognition System

Follow these steps to download and run the project locally:

## Step 1: Download the Project

1. Go to the GitHub repository: https://github.com/bodhisathwa/lpr_india.git
2. Click the green **Code** button
3. Select **Download ZIP**
4. Extract the ZIP file to your preferred location

## Step 2: Open in VS Code

1. Open Visual Studio Code
2. Go to **File > Open Folder**
3. Navigate to the extracted `indian-lpr` folder and click **Select Folder**

## Step 3: Set Up Environment

\`\`\`bash

# Open a terminal in VS Code (Terminal > New Terminal)

# Create a virtual environment

python -m venv venv

# Activate the virtual environment

# For Windows:

venv\Scripts\activate

# For macOS/Linux:

# source venv/bin/activate

# Install dependencies

pip install -r requirements.txt

# Create required directories

mkdir -p temp database
\`\`\`

## Step 4: Configure Azure API

1. Create a \`.env\` file in the project root with:
   \`\`\`
   AZURE_API_KEY=your_azure_api_key
   AZURE_ENDPOINT=your_azure_endpoint_url
   \`\`\`
2. To get these values:

   - Sign in to [Azure Portal](https://portal.azure.com)
   - Create or access your Computer Vision resource
   - Go to **Keys and Endpoint** section
   - Copy the key and endpoint URL

## Step 5: Test Azure Connection

\`\`\`bash

# Run the test script to verify your Azure connection

python test_azure_connection.py
\`\`\`

## Step 6: Run the Application

\`\`\`bash

# Start the Streamlit application

streamlit run app.py
\`\`\`

## Step 7: Using the Application

1. Open your browser (Streamlit will provide a URL, typically http://localhost:8501)
2. Choose your input method (File Upload or External Camera)
3. Upload an image containing an Indian license plate
4. View the recognition results

## Troubleshooting

- **OCR not working**: Verify your Azure API key and endpoint in the \`.env\` file
- **Missing modules**: Run \`pip install -r requirements.txt\` again
- **Image processing errors**: Ensure the uploaded image is clear and well-lit
- **\"No module named 'azure'\"**: Try running \`pip install azure-cognitiveservices-vision-computervision\` separately

## Project Structure Overview

- \`app.py\`: Main Streamlit application
- \`services/\`: Core services (Azure OCR, database, image processing)
- \`utils/\`: Helper utilities (preprocessing, validators)
- \`config/\`: Configuration files and constants

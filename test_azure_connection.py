# test_azure_connection.py
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        client = ComputerVisionClient(
            os.getenv("AZURE_ENDPOINT"),
            CognitiveServicesCredentials(os.getenv("AZURE_API_KEY"))
        )
        print("✅ Azure connection successful!")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()
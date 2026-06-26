
import os
import base64
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from config.settings import get_settings

settings = get_settings()


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')


def test_mistral_ocr(image_path):
    """Test Mistral OCR on the given image."""
    print(f"Testing Mistral OCR on: {image_path}")
    print("=" * 60)
    
    if not os.path.exists(image_path):
        print(f"ERROR: File not found: {image_path}")
        return None

    try:
        image_b64 = encode_image_to_base64(image_path)
        print(f"Image encoded successfully.")
        
        import requests

        headers = {
            "Authorization": f"Bearer {settings.MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "pixtral-large-latest",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all text from this receipt or document. Return only the extracted text, no explanations."},
                        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_b64}"}
                    ]
                }
            ],
            "temperature": 0,
            "max_tokens": 2048
        }

        print(f"Sending request to Mistral OCR...")

        response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            extracted_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            print("SUCCESS! Extracted text:")
            print("-" * 60)
            print(extracted_text)
            print("-" * 60)
            return extracted_text
        else:
            print(f"ERROR: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Mistral OCR")
    parser.add_argument("image", nargs="?", help="Path to the image file to OCR")
    args = parser.parse_args()
    
    if args.image:
        test_mistral_ocr(args.image)
    else:
        print("Usage: python test_mistral_ocr.py <path_to_image>")
        print("\nExample: python test_mistral_ocr.py sample_images/receipt.jpg")
        print("\nOr if you don't have an image, let's check if the API key is working...")
        
        # Test API key by checking settings
        print(f"\nMISTRAL_API_KEY loaded: {settings.MISTRAL_API_KEY[:10]}...")
        print(f"OCR_ENGINE: {settings.OCR_ENGINE}")
        print("API key looks okay!")

import os
import json

from dotenv import load_dotenv

from google import genai
from google.oauth2.service_account import Credentials
from google.cloud import vision

load_dotenv()

SERVICE_ACCOUNT_FILE_PATH = './credentials/service_account.json'
if os.path.exists(SERVICE_ACCOUNT_FILE_PATH):
    credentials = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE_PATH,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
    
    with open(SERVICE_ACCOUNT_FILE_PATH, 'r') as f:
        sa = json.load(f)

    PROJECT_ID = sa['project_id']
    # Init google cloud vision client
    vision_client = vision.ImageAnnotatorClient(credentials=credentials)
else:
    credentials = None
    PROJECT_ID = None

REGION = 'global'

# Select Gemini model version
GEMINI_MODEL_NAME = os.getenv('GEMINI_MODEL_NAME')


def ask(content, authen='api-key'):
    if authen == 'api-key':
        print('GCP Gemini auth via api-key')
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    elif authen == 'sa':
        print('GCP Gemini auth via service account')
        client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=REGION,
            credentials=credentials
        )
    
    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=content
    )

    # print(response)

    return response

def get_text_from_image(image_path):
    with open(image_path, 'rb') as f:
        image_content = f.read()
    response = vision_client.text_detection(image=vision.Image(content=image_content))
    texts = response.text_annotations

    return texts

if __name__ == '__main__':
    question = "Who is CEO of Apple Inc."
    image_path = './images/text-image-title.png'

    answer = ask(question, authen='sa')
    print('Answer:', answer)

    text_from_image = get_text_from_image(image_path)
    print('Detected texts:', text_from_image)
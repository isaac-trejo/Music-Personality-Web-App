import os 

from dotenv import load_dotenv

load_dotenv()

SP_CLIENT_ID = os.getenv('SP_CLIENT_ID')
SP_CLIENT_SECRET = os.getenv('SP_CLIENT_SECRET')
SP_REDIRECT_URI = os.getenv('SP_REDIRECT_URI')
HF_TOKEN = os.getenv('HF_TOKEN')
GENIUS_CLIENT_SECRET = os.getenv('GENIUS_CLIENT_SECRET')
GENIUS_TOKEN = os.getenv('GENIUS_TOKEN')

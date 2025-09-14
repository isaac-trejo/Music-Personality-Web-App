from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os 
# from config import HF_TOKEN

load_dotenv()

# NLP client to analyze song lyrics  
hf_client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv('HF_TOKEN')
)

""" Input is lyrics.
    Returns list of tuples of emotional probabilities 
    *Note: Max token input = 512, roughly 2048 chars """
def lyric_emotion_info(lyrics: str) -> list | None:
    if not lyrics:
        return None

    result = hf_client.text_classification(
        text=lyrics,
        model="SamLowe/roberta-base-go_emotions",
    )
    emotion_list = [(emotion['label'], emotion['score']) for emotion in result]
    print(emotion_list)

    return emotion_list 

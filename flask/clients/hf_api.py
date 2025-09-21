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
def lyric_emotion_info(chunked_lyrics: list) -> list | None:
    if not chunked_lyrics:
        return None
    
    emotion_pair_list = list()
    for chunk in chunked_lyrics:
        emotion_result = hf_client.text_classification(
            text=chunk,
            model="SamLowe/roberta-base-go_emotions",
        )
        emotion_pair_list = [(emotion['label'], emotion['score']) for emotion in emotion_result]
    
    print(emotion_pair_list)
    return emotion_pair_list 

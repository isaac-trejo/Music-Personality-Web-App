import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

def main():
    hf_token = os.getenv("HF_TOKEN")
    hf_client = InferenceClient(
        provider="hf-inference",
        api_key=hf_token,
    )


    result = hf_client.text_classification(
        "The industry can hate me, fuck 'em all and they mama",
        model="SamLowe/roberta-base-go_emotions",
    )
    emotion_info = [(emotion['label'], emotion['score']) for emotion in result]
    return emotion_info

main()
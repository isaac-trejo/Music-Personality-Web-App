import os 
from dotenv import load_dotenv
from lyricsgenius import Genius
# from config import GENIUS_TOKEN

load_dotenv()

# Genius Client 
genius = Genius(
    access_token=os.getenv('GENIUS_TOKEN'),
    remove_section_headers=True,    # Removes "Chorus" & "Verse" headers
    excluded_terms=["(Remix)", "(Live)"]    # Only original song searches
)

""" Input is song name and artist and uses Genius client to 
    search.
    Returns song lyrics as string. """
def get_lyrics(song_name: str, artist: str) -> str | None:
    song = genius.search_song(song_name, artist)
    return song.lyrics if song else None

""" Input is entire song lyrics and portions lyrics into elements 
    in a list.
    Returns seperated lyrics chunks in list"""
def chunk_lyrics(lyrics: str) -> list | None:
    if not lyrics:
        return None

    # Characters per chunk based off half of SamLowe/roberta-base-go_emotions
    # max 512 token input and white space accounted 
    chars_per_chunk = 1024 
    token_chunks = list()
    lines = list()  

    lyrics = lyrics.replace(')', '').replace('(', '')   # Remove paranthesis
    lines = lyrics.split('\n')  # separate lyrics by lines  

    temp_string = ''
    char_count = 0
    # Add chunks of lyrics into list
    for line in lines:
        temp_string += line + ' '   # added space to sperate appended lines
        char_count += len(line) + 1     # + 1 b/c added space ^
        if char_count >= chars_per_chunk:
            token_chunks.append(temp_string)
            temp_string = ''
            char_count = 0

    # Handle left over lines of lyrics 
    if temp_string.strip():
        token_chunks.append(temp_string)

    for index, chunk in enumerate(token_chunks):
        print(f'{index}: {chunk}\n')

    return token_chunks

def normalize_emotions_percent(emotion_list: list) -> list | None:
    if not emotion_list:
        return None
    elif len(emotion_list) < 2:
        return emotion_list
    
    normalized_emotions = list()

    total_score = sum(score for _, score in emotion_list)
    if total_score == 0:
        return [(emotion, 0.0) for emotion, _ in emotion_list]
    
    normalized_emotions = [
        (emotion, (score / total_score) * 100)
        for emotion, score in emotion_list
    ]

    return normalized_emotions
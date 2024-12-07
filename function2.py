def translate_reviews(reviews, src_lang='ko', dest_lang='en'):
    """
    리뷰를 한국어에서 영어로 번역하거나 영어에서 한국어로 번역.
    """
    translator = Translator()
    translated_reviews = []
    for review in reviews:
        translated = translator.translate(review, src=src_lang, dest=dest_lang).text
        translated_reviews.append(translated)
    return translated_reviews

def analyze_sentiment_sentences(sentences):
    """
    Hugging Face 모델을 이용해 각 문장의 감정 분석.
    """
    sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    results = []
    for sentence in sentences:
        if sentence.strip():  # 빈 문장은 건너뜀
            result = sentiment_pipeline(sentence)[0]
            label = result['label']
            stars = int(label.split()[0])  # 예: '5 stars' -> 5
            results.append((sentence.strip(), stars))
    return results
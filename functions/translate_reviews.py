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


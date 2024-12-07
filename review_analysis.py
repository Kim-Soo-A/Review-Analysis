import re
from transformers import pipeline
from googletrans import Translator

def load_reviews_from_file(file_path):
    """
    텍스트 파일에서 리뷰를 불러옴.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        reviews = file.readlines()
    return [review.strip() for review in reviews if review.strip()]

def split_into_sentences(text):
    """
    텍스트를 문장 단위로 분리.
    """
    return re.split(r'[.!?]', text)

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

def classify_pros_and_cons(sentences_with_ratings):
    """
    별점을 기준으로 문장 단위 장점(4~5점)과 단점(1~3점) 분류.
    """
    pros = [sentence for sentence, stars in sentences_with_ratings if stars >= 4]
    cons = [sentence for sentence, stars in sentences_with_ratings if stars <= 3]
    return pros, cons

def calculate_average_rating(star_ratings):
    """
    별점의 평균 계산.
    """
    return sum(star_ratings) / len(star_ratings)

if __name__ == "__main__":
    # Step 1: 리뷰 파일 불러오기
    file_path = input("리뷰 파일 경로를 입력하세요 (예: reviews.txt): ")
    reviews = load_reviews_from_file(file_path)

    # Step 2: 리뷰 번역 (한국어 -> 영어)
    translated_reviews = translate_reviews(reviews, src_lang='ko', dest_lang='en')

    # Step 3: 문장 단위로 나누기 및 감정 분석
    all_pros, all_cons = [], []
    star_ratings = []
    for review in translated_reviews:
        sentences = split_into_sentences(review)
        sentences_with_ratings = analyze_sentiment_sentences(sentences)
        pros, cons = classify_pros_and_cons(sentences_with_ratings)
        all_pros.extend(pros)
        all_cons.extend(cons)
        star_ratings.extend([stars for _, stars in sentences_with_ratings])

    # Step 4: 장단점 한국어 번역
    pros_in_korean = translate_reviews(all_pros, src_lang='en', dest_lang='ko')
    cons_in_korean = translate_reviews(all_cons, src_lang='en', dest_lang='ko')

    # Step 5: 평균 별점 계산
    average_rating = calculate_average_rating(star_ratings)
    print(f"\n평균 별점: {average_rating:.1f} stars")

    # Step 6: 결과 출력
    print("\n[장점]:")
    # 장점을 최대 3개로 제한
    for idx, pro in enumerate(pros_in_korean[:3], 1):  # 최대 3개
        print(f"{idx}. {pro}")

    print("\n[단점]:")
    # 단점을 최대 3개로 제한
    for idx, con in enumerate(cons_in_korean[:3], 1):  # 최대 3개
        print(f"{idx}. {con}")

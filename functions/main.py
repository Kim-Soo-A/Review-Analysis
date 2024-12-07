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

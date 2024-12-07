def load_reviews_from_file(file_path):
    """
    텍스트 파일에서 리뷰를 불러옴.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        reviews = file.readlines()
    return [review.strip() for review in reviews if review.strip()]

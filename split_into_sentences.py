def split_into_sentences(text):
    """
    텍스트를 문장 단위로 분리.
    """
    return re.split(r'[.!?]', text)

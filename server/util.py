# https://research.arizona.edu/faq/what-do-you-mean-when-you-say-use-title-case-proposalproject-titles
def snake_to_title_case(text: str) -> str:
    if not text: return ""
    minor_words = set([
        'a', 'an', 'the',
        'and', 'as', 'but', 'for', 'if', 'nor', 'or', 'so', 'yet',
        'at', 'by', 'in', 'of', 'off', 'on', 'per', 'to', 'up', 'via'
    ])
    res = " ".join(
        map(
            lambda word: word.capitalize() if word not in minor_words else word,
            text.lower().split("_")
        )
    )
    return res[0].upper() + res[1:]

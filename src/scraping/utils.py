import transliterate
__all__ = [
    'translit',
]


def translit(text: str):
    return transliterate.translit(text, reversed=True)

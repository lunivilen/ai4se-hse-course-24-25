from data_prepair.const_variables import CONTRACTION_MAPPING, RE_URL, RE_REPEATS, RE_SPECIALS, RE_PATTERNS
import unicodedata
import re


def expand_contraction(text: str) -> str:
    """Расшифровывает сокращения"""
    specials = ["’", "‘", "´", "`", "'"]

    for s in specials:
        text = text.replace(s, "'")
        text = ' '.join([CONTRACTION_MAPPING[t] if t in CONTRACTION_MAPPING else t for t in text.split(" ")])
    return text


def normalize_unicode(text: str) -> str:
    """Нормализует юникод"""
    s = unicodedata.normalize("NFKC", text)
    return ''.join(ch for ch in s if not unicodedata.category(ch).startswith('C'))


def fix_bad_words(text: str) -> str:
    for target, patterns in RE_PATTERNS.items():
        for pat in patterns:
            text = text.replace(pat, target)
    return text


def clean_one(message: str) -> str:
    """Очищает одну запись"""
    message = normalize_unicode(message.lower())

    # удаляем URL
    message = RE_URL.sub(" ", message)

    # унификация пробелов
    message = re.sub(r'\s+', ' ', message).strip()

    # раскрытие сокращений
    message = expand_contraction(message)

    # исправление специально исправленных плохих слов
    message = fix_bad_words(message)

    # удаление повторяющихся символов
    message = RE_REPEATS.sub(r'\1', message)

    # удаление спецсимволов
    message = RE_SPECIALS.sub(' ', message)

    # финальная нормализация пробелов
    message = re.sub(r'\s+', ' ', message).strip()
    return message

import random
import re
import unicodedata
from pathlib import Path
from getRssFeed import getNews

BASE_DIR = Path(__file__).resolve().parent
WORDS_DIR = BASE_DIR.parent / "wordsData"


def normalize(text):
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def load_file(file_name):
    path = WORDS_DIR / file_name
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]


def clean_sensible_news(news_list, sensible_words):
    if not sensible_words:
        return news_list
    escaped = [re.escape(normalize(w)) for w in sensible_words]
    pattern = re.compile(r"\b(" + "|".join(escaped) + r")\b", re.IGNORECASE)
    return [n for n in news_list if not pattern.search(normalize(n))]





def clean_edge_words(text):


    bad_endings = (
        r"\b(de|da|do|dos|das|em|no|na|nos|nas|com|para|por|que|mas|e|ou|porém|"
        r"entretanto|todavia|o|a|os|as|um|uma|uns|umas)\s*$"
    )
    bad_starters = r"^\s*(que|e|ou|mas|porém|entretanto|todavia|onde|como)"

    # Limpa conectores soltos nas pontas
    text = re.sub(bad_endings, "", text, flags=re.IGNORECASE).strip()
    text = re.sub(bad_starters, "", text, flags=re.IGNORECASE).strip()

    # Remove qualquer pontuação (!, ?, ., ,) das extremidades
    text = re.sub(r"^[\s,;:\-–.!?]+|[\s,;:\-–.!?]+$", "", text).strip()

    return text

def split_smart_clause(headline):
    parts = [p.strip() for p in re.split(r"[:;\-–]", headline) if p.strip()]
    if len(parts) >= 2:
        return parts[0], parts[-1]

    parts_comma = [p.strip() for p in headline.split(",") if p.strip()]
    if len(parts_comma) >= 2:
        return parts_comma[0], parts_comma[-1]

    words = headline.split()
    if len(words) >= 6:
        mid = len(words) // 2
        return " ".join(words[:mid]), " ".join(words[mid:])

    return headline, headline


def get_excuse_headline():
    places = load_file("saltWordsPlaces_PTBR.txt")
    objects = load_file("saltWordsObjects_PTBR.txt")
    chars = load_file("saltWordsChars_PTBR.txt")


    place = random.choice(places) if places else "na redação"
    obj = random.choice(objects) if objects else "um microfone"
    char = random.choice(chars) if chars else "um suspeito"


    templates = [
        f"Sem sinal de internet {place}: repórter foi atingido por {obj}.",
        f"Transmissão {place} interrompida após {char} hackear nossos sistemas.",
        f"Boletim cancelado {place}: {char} recusou entrevista e arremessou {obj}.",
        f"Edição suspensa: {char} disse para tirar a matéria do ar {place}.",
        f"Correspondente {place} perdeu o sinal enquanto tentava desviar de {obj}.",
        f"Sem notícias {place}: {char} roubou o sinal de internet com {obj}.",
    ]

    return random.choice(templates)


def get_dada_headline(news_list):
    if len(news_list) < 2:
        return get_excuse_headline()

    part1, part2 = None, None

    for _ in range(10):
        line1, line2 = random.sample(news_list, 2)

        p1, _ = split_smart_clause(line1)
        _, p2 = split_smart_clause(line2)

        p1 = clean_edge_words(p1)
        p2 = clean_edge_words(p2)

        if len(p1.split()) >= 3 and len(p2.split()) >= 3:
            part1, part2 = p1, p2
            break


    if not part1 or not part2:
        return get_excuse_headline()


    words_part2 = part2.split()
    if words_part2:
        first_word = words_part2[0]
        if not first_word.isupper():
            words_part2[0] = first_word.lower()
        part2_clean = " ".join(words_part2)
    else:
        part2_clean = part2

    # Lógica de conexão
    starts_with_prep = re.match(
        r"^(para|com|por|em|no|na|sobre|segundo|durante)\b",
        part2_clean,
        re.IGNORECASE,
    )

    if starts_with_prep:
        connector = ","
    else:
        connector = random.choice([",", " -", " enquanto", " e"])

    headline = f"{part1}{connector} {part2_clean}".strip()
    headline = re.sub(r"\s+,", ",", headline)
    headline = re.sub(r"\s+", " ", headline)

    if not headline.endswith((".", "!", "?")):
        headline += "."

    return headline


def getOneNews():
    sensible = load_file("sensibleThemes_PTBR.txt")
    news = getNews()
    clean_news = clean_sensible_news(news, sensible)

    return get_dada_headline(clean_news)


if __name__ == "__main__":
    print(getOneNews())
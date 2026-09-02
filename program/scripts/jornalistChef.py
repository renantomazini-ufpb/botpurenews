from .getRssFeed import getNews
from pathlib import Path
import random
import re
import unicodedata
#import hashlib

#smells bad? Mas confia
BASE_DIR = Path(__file__).resolve().parent
WORDS_DIR = BASE_DIR.parent / "wordsData"


def normalize(text):
    text = unicodedata.normalize('NFD', text.lower())
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn')


def load_file(file_name):
    path = WORDS_DIR / file_name
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]


def clean_sensible_news(news_list, sensible_words):
    if not sensible_words:
        return news_list
    escaped = [re.escape(normalize(w)) for w in sensible_words]
    pattern = re.compile(r'\b(' + '|'.join(escaped) + r')\b', re.IGNORECASE)
    return [n for n in news_list if not pattern.search(normalize(n))]


def split_smart_clause(headline):

    parts = [p.strip() for p in re.split(r'[:;\-–,.]', headline) if p.strip()]
    if len(parts) >= 2:
        return parts[0], parts[-1]
    

    words = headline.split()
    mid = len(words) // 2
    return " ".join(words[:mid]), " ".join(words[mid:])



def getOneNews():
    sensible = load_file("sensibleThemes_PTBR.txt")
    news = getNews()
    clean_news = clean_sensible_news(news, sensible)
    
    return get_dada_headline(clean_news)


if __name__ == "__main__":
    print(getOneNews())




def clean_edge_words(text):

    bad_endings = r'\b(de|da|do|dos|das|em|no|na|nos|nas|com|para|por|que|mas|e|ou|porém|entretanto|todavia)\s*$'

    bad_starters = r'^\s*(que|e|ou|mas|porém|entretanto|todavia|onde|como)'

    text = re.sub(bad_endings, '', text, flags=re.IGNORECASE).strip()
    text = re.sub(bad_starters, '', text, flags=re.IGNORECASE).strip()
    return text

def get_dada_headline(news_list):
    if len(news_list) < 2:
        return "Sem notícias suficientes"

    line1, line2 = random.sample(news_list, 2)

    part1, _ = split_smart_clause(line1)
    _, part2 = split_smart_clause(line2)


    part1 = clean_edge_words(part1)
    part2 = clean_edge_words(part2)

    if not part1 or not part2:
        return "Sem notícias suficientes"

    connector = random.choice([",", ";", " e"])
    part2_clean = part2[0].lower() + part2[1:]

    headline = f"{part1}{connector} {part2_clean}".strip()
    

    headline = re.sub(r'\s+,', ',', headline)
    headline = re.sub(r'\s+', ' ', headline)

    return headline
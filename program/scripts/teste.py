import random
import re
import unicodedata
from pathlib import Path
from getRssFeed import getNews

# ========================
# Versão simplificada da antiga, feita com base em muito enxugamento e ajuda de bots
# ========================

base_dir = Path(__file__).resolve().parent
words_dir = base_dir.parent / "wordsData"
SENSIBLE_PATH = words_dir / "sensibleThemes_PTBR.txt"


def load_list(path):
    with open(path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]


def load_words():
    def f(name): return load_list(words_dir / name)
    return {
        "chars": f("saltWordsChars_PTBR.txt"),
        "places": f("saltWordsPlaces_PTBR.txt"),
        "objects": f("saltWordsObjects_PTBR.txt"),
        "adjectives": f("saltWordsAdjectives_PTBR.txt"),
    }


# Isso foi o começo

def normalize(text):
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn')


def filter_sensible(news, bad_words):
    patterns = [
        re.compile(rf'\b{re.escape(normalize(w))}\b')
        for w in bad_words
    ]

    clean = []
    for n in news:
        t = normalize(n)
        if not any(p.search(t) for p in patterns):
            clean.append(n)

    return clean


def split_title(t):
    w = t.split()
    if len(w) < 4:
        return t, ""
    m = len(w)//2
    return " ".join(w[:m]), " ".join(w[m:])


def mix(news):
    n1, n2 = random.sample(news, 2)
    p1, _ = split_title(n1)
    _, p2 = split_title(n2)
    return f"{p1}, {p2}"

def mixmix(news):
    n1, n2, n3 = random.sample(news, 3)

    p1, _ = split_title(n1)
    mid1, mid2 = split_title(n2)
    _, p3 = split_title(n3)

    middle = mid2 if mid2 else mid1

    return f"{p1}, {middle}, {p3}"

def with_char(news, chars):
    base = mix(news)
    return f"{base}, diz {random.choice(chars)}"


def with_place(news, places):
    base = mix(news)
    return f"{base} em {random.choice(places)}"


def word_swap(title, pool):
    words = title.split()

    idxs = [i for i, w in enumerate(words) if len(w) > 4]
    if not idxs:
        return title

    for _ in range(2):
        i = random.choice(idxs)
        words[i] = random.choice(pool)

    return " ".join(words)



def dada(news):
    words = [w for n in news for w in n.lower().split() if len(w) > 4]

    for _ in range(10):
        w = random.choice(words)
        matches = [n for n in news if w in n.lower()]

        if len(matches) < 2:
            continue

        n1, n2 = random.sample(matches, 2)

        p1 = n1.split(w)[0].strip()
        p2 = n2.split(w)[-1].strip()

        if p1 and p2:
            return f"{p1} {w} {p2}"

    return None



def clean(t):
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'\s+,', ',', t)
    return t.strip()


def getOneNews():
    news = getNews()

    sensible = load_list(SENSIBLE_PATH)
    news = filter_sensible(news, sensible)

    words = load_words()

    fallback = [
        "Jornalismo de qualidade exige discursos",
        "O estágiario cortou nossa internet!",
        "Jornalista encontrado procastinando em casa!",
        "Pix sumiu, servidor caiu",
        "Garfo encontrado na cozinha!",
        "Revolta das máquinas: Bot de notícias se recusa a trabalhar",
        "'tamo' de atestado",
        "tropeçaro nos cabos",
        "O que é lambimia?",
        "Revoltz",
        ":) Tenha um bom dia!",
        "Hackeram meu windows",
        "parem as máquinas!",
        "Jornalismo ou esquema de pirâmede? Descubra",
        "Pix sumiu, servidor caiu"
    ]

    if len(news) < 2:
        return random.choice(fallback)

    gens = [
        lambda: mix(news),
        lambda: mix(news),
        lambda: mix(news),
        lambda: mix(news),
        lambda: with_char(news, words["chars"]),
        lambda: with_place(news, words["places"]),
        lambda: dada(news),
    ]

    for _ in range(5):
        t = random.choice(gens)()

        if not t:
            continue
        if random.random() < 0.4:
            pool = words["objects"] + words["adjectives"]
            t = word_swap(t, pool)

        return clean(t)

    return random.choice(news)
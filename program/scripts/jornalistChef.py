from .getRssFeed import getNews
from pathlib import Path
import random
import re
import unicodedata

#smells bad? Mas confia

base_dir = Path(__file__).resolve().parent
words_dir = base_dir.parent / "wordsData"
caminho = words_dir / "sensibleThemes_PTBR.txt"


def loadSensibleThemes(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]


def loadWordLists():
    def load(file_name):
        path = words_dir / file_name
        with open(path, 'r', encoding='utf-8') as f:
            return [
                l.strip()
                for l in f
                if l.strip() and not l.startswith("#")
            ]

    return {
        "chars": load("saltWordsChars_PTBR.txt"),
        "places": load("saltWordsPlaces_PTBR.txt"),
        "free": load("saltWordsFree_PTBR.txt"),
        "objects": load("saltWordsObjects_PTBR.txt"),
        "animals": load("animalsPTBR.txt"),
    }



def normalize(text):
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn')


def cleanSensibleNews(news_list, sensible_words):
    patterns = [
        re.compile(rf'\b{re.escape(normalize(w))}\b')
        for w in sensible_words
    ]

    clean = []
    for n in news_list:
        text = normalize(n)

        if not any(p.search(text) for p in patterns):
            clean.append(n)

    return clean



def maybeAddPlace(title, places):
    if not places or random.random() > 0.20:
        return title

    place = random.choice(places)
    if re.search(r'\bem\s+\w+', title.lower()):
        return title

    return f"{title} em {place}"


def maybeAddChar(title, chars):
    if not chars or random.random() > 0.20:
        return title

    char = random.choice(chars)

    templates = [
        f"{title}, diz {char}",
        f"{title}, afirma {char}",
        f"{title}, segundo {char}",
    ]

    return random.choice(templates)


def maybeSoftTwist(title):
    if random.random() > 0.25:
        return title

    twists = [
            "e bolsa reage",
            "analistas comentam",
            "e tudo muda",
            "e surpreende",
            "e termina de forma inesperada",
            "e causa confusão",
            "e mercado reage",
            "e mercado reage",
            "mas a que custo?"
    ]

    return f"{title} {random.choice(twists)}"


def maybeWordSwap(title):
    if random.random() > 0.2:
        return title

    words = title.split()

    if len(words) < 5:
        return title

    idx = random.randint(1, len(words)-2)

    # troca leve (embaralha palavras longas)
    if len(words[idx]) > 6:
        words[idx] = words[idx][::-1]

    return " ".join(words)

def fixConnectiveCollisions(text):
    # Lista de substituições para conectivos grudados
    substitutions = [
        (r'\bcom\s+no\b', 'no'),        # "com no" -> "no"
        (r'\bcom\s+na\b', 'na'),        # "com na" -> "na"
        (r'\bcom\s+o\b', 'com o'),      # Garante espaço correto
        (r'\bem\s+no\b', 'no'),         # "em no" -> "no"
        (r'\bde\s+do\b', 'do'),         # "de do" -> "do"
        (r'\bpara\s+pro\b', 'pro'),     # "para pro" -> "pro"
        (r'\bcom\s+com\b', 'com'),      # "com com" -> "com"
        (r'\bque\s+que\b', 'que'),      # "que que" -> "que"
        (r'\bcom\s+em\b', 'em'),        # "com em" -> "em"
    ]
    
    for pattern, replacement in substitutions:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text



def finalize(title):
    title = fixConnectiveCollisions(title) 

    title = re.sub(r'\s+', ' ', title).strip()
    title = re.sub(r'\s+,', ',', title)
    title = re.sub(r',\s*,', ',', title)

    if title:
        title = title[0].upper() + title[1:]

    title = re.sub(r'\b(do|da|de|para|com|em)\s*,', ',', title, flags=re.IGNORECASE) #nao consigo juntar os dois pq??
    title = re.sub(r'\b(de|para|com|em|por|sobre|após|enquanto)\s*$', '', title, flags=re.IGNORECASE) #nao pode sobrar

    return title

def getOneNews():
    sensible = loadSensibleThemes(caminho)
    wordLists = loadWordLists()

    news = getNews()
    news = cleanSensibleNews(news, sensible)

    if len(news) < 2:
        return "Sem notícias suficientes"

    title = mixHeadlinesV3(news)

    if not title:
        n1, n2 = random.sample(news, 2)
        title = f"{n1.split(':')[0]}, {' '.join(n2.split()[-5:])}"

 
    if random.random() < 0.15:
        title = maybeAddPlace(title, wordLists["places"])

    if random.random() < 0.35:
        title = maybeAddChar(title, wordLists["chars"])

    if random.random() < 0.15:
        title = maybeSoftTwist(title)


    if random.random() < 0.05:
        title = maybeWordSwap(title)

    title = fillBrokenConnectives(title, wordLists)

    title = fixWeirdStructures(title)

    title = removeBadConnectors(title)
    title = polishHeadline(title)

    title = addHumanFlavor(title)

    title = ensureStrongEnding(title) 
    title = removeBrokenComparisons(title)
    title = finalize(title)

    return title

def maybeApplyNewsStyle(title):
    if random.random() > 00.40:
        return title

    return applyNewsStyle(title)

def forceChange(title, wordLists):
    # tomara que funcione

    if wordLists["places"]:
        return f"{title} em {random.choice(wordLists['places'])}"

    if wordLists["chars"]:
        return f"{title}, diz {random.choice(wordLists['chars'])}"

    return title + " (atualizado)"


def ensureStrongEnding(title):
    if not title:
        return title

    weak_words = [
        "de", "do", "da", "dos", "das",
        "para", "pra", "pro",
        "com", "sem",
        "em", "no", "na", "nos", "nas",
        "por", "sobre",
        "e", "ou", "mas",
        "o", "a", "os", "as", "um", "uma", "que"
    ]

    words = title.strip().split()

    if not words:
        return title

    last = words[-1].lower()


    if last in weak_words:
        words.pop()


    if len(words) < 3:
        return " ".join(words)

   
    if re.match(r'^[^a-zA-ZÀ-ÿ]+$', words[-1]):
        words.pop()

    if random.random() < 0.25:
        endings = [
            "entenda",
            "veja detalhes",
            "diz especialista",
            "segundo analistas",
            "e repercute",
            "e gera reação",
        ]

        # só adiciona se já não parecer completo
        if words[-1].lower() not in ["reação", "detalhes", "especialista"]:
            words.append(random.choice(endings))

    return " ".join(words)

def makePlotTwistNews(news_list):
    new_news = []

    for n in news_list:
        twist = random.choice([
            "e bolsa reage",
            "analistas comentam",
            "e tudo muda",
            "e surpreende",
            "e termina de forma inesperada",
            "e causa confusão",
            "e mercado reage",
            "e mercado reage",
            "e mercado reage",
            "e mercado reage",
            "mas a que custo?",
        ])

        new_news.append(f"{n}, {twist}")

    return new_news


def getWordMatches(word, lines):
    matches = []
    for l in lines:
        words = l.lower().split()
        if word in words:
            matches.append(l)
    return matches


def getCommonWord(lines):
    pool = []

    for l in lines:
        for w in l.lower().split():
            w = re.sub(r'[^\w]', '', w)
            if len(w) > 4:  # evita lixo tipo "de", "com"
                pool.append(w)

    random.shuffle(pool)

    for word in pool:
        matches = getWordMatches(word, lines)
        if len(matches) >= 2:
            return word, matches

    return None, None

def mixHeadlines(lines):
    word, matches = getCommonWord(lines)

    if not word:
        return None

    random.shuffle(matches)

    for _ in range(5):
        if len(matches) < 2:
            return None

        l1, l2 = random.sample(matches, 2)

        if l1 == l2:
            continue

        parts1 = re.split(rf'\b{re.escape(word)}\b', l1, flags=re.IGNORECASE)
        parts2 = re.split(rf'\b{re.escape(word)}\b', l2, flags=re.IGNORECASE)

        if len(parts1) < 2 or len(parts2) < 2:
            continue

        p1 = " ".join(parts1[0].split()[:5])
        p2 = " ".join(parts2[-1].split()[-5:])

        if len(p1.split()) < 2 or len(p2.split()) < 2:
            continue

        connector = random.choice([",", "após", "enquanto"])
        candidate = f"{p1} {connector} {p2}"

        # evita clone
        if candidate != l1 and candidate != l2:
            return candidate

    return None

#copia e cola da net
def fillBrokenConnectives(title, wordLists):
    pool = (
        wordLists.get("chars", []) +
        wordLists.get("free", [])
    )

    if not pool:
        return title
    pattern = r'\b(o|a|os|as|um|uma)\b\s*([,;:.!?])'

    def repl(m):
        return f"{m.group(1)} {random.choice(pool)}{m.group(2)}"

    title = re.sub(pattern, repl, title, flags=re.IGNORECASE)

    pattern_end = r'\b(o|a|os|as|um|uma)\s*$'
    title = re.sub(
        pattern_end,
        lambda m: f"{m.group(1)} {random.choice(pool)}",
        title,
        flags=re.IGNORECASE
    )

    return title



def applyNewsStyle(title):
    patterns = [



        "{}; mercado reage bem",
        "{}; mercado reage mal",
        "{}; veja o vídeo",
        "{}; mais no site",
        "{}: entenda o caso",

        "{}; veja detalhes",
        "{} e mercado reage",
        "{} e viraliza",
        "{} e gera reação",

        "{} e repercute nas redes",
        "{} e levanta debate",
        "{}, argumentam especialistas",
        "{} surpreende especialistas",
        "{}; veja nas redes",
        "{} chama atenção",
        "{} vira destaque",
        "{}, veja as imagens",
        "{} #bot",

        "{} #purenews",

        "{} #dadaismo",

        "{}; apura reporter",
        "{}; deve ser IA, apura reporter",

        "{} 😨",
        "{}; :)",
        "{}; é 13🌟!",
        "{}; :)",
        "{} 🙄​",
        "{} 😁​​",
        "{} 🤪​",
        "{} 🤪​",
        "{} :P",
        "{} :O",
        "{} ¯\\_(ツ)_/¯",
        "{} !",
        "{} !?",
        "{} ?",

    ]

    pattern = random.choice(patterns)
    return pattern.format(title)





#obrgiado copilot, por me deixar confuso
def mixHeadlinesV2(lines):
    if len(lines) < 2:
        return None

    l1, l2 = random.sample(lines, 2)

    w1 = l1.split()
    w2 = l2.split()

    if len(w1) < 5 or len(w2) < 5:
        return None

    part1 = " ".join(w1[:random.randint(4, 7)])


    part2 = " ".join(w2[-random.randint(4, 7):])

    connector = random.choice([
        ",",
        "e",
        ":",
    ])

    candidate = f"{part1} {connector} {part2}"

    if candidate != l1 and candidate != l2:
        return candidate

    return None

def polishHeadline(title):
    fixes = [
        # remove conectivo quebrado
        (r'\b(de|para|com|em|após|enquanto)\s*([,;:.!?])', r'\2'),

        # remove duplicações
        (r'\b(\w+)\s+\1\b', r'\1'),

        # corrige pontuação
        (r'\s+,', ','),
        (r',\s*,', ','),
        (r'\s+;', ';'),

        # evita início ruim
        (r'^(e|mas|ou)\s+', ''),

        # corrige espaços
        (r'\s+', ' '),
    ]

    for pattern, repl in fixes:
        title = re.sub(pattern, repl, title, flags=re.IGNORECASE)

    return title.strip()

def addHumanFlavor(title):
    if random.random() > 0.35:
        return title

    additions = [
        "diz especialista",
        "aponta estudo",
        "segundo governo",
        "veja o que se sabe",
        "entenda",
        "veja detalhes",
    ]

    if "," in title:
        return f"{title}, {random.choice(additions)}"
    else:
        return f"{title} {random.choice(additions)}"

def fixWeirdStructures(text): #aaaaa
    fixes = [

        (r'\b(de|para|com|em|após|enquanto)\s*([,;:.!?])', r'\2'),


        (r'\b(\w+)\s+\1\b', r'\1'),


        (r'\b(enquanto|após)\s+(para|com|de)\b', r'\2'),
        (r'\b(para|com|de)\s+(enquanto|após)\b', r'\1'),


        (r'\bnão\s*;', 'não'),


        (r';\s*;', ';'),
        (r',\s*;', ';'),
        (r';\s*,', ';'),
        (r'^(e|mas|ou)\s+', ''),

        # esaaaaaa
        (r'\s+', ' '),
    ]

    for pattern, repl in fixes:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    return text.strip()

def mixHeadlinesV3(lines): #esse foi revisado, sim, chamei IA, chefe e até professor!
    if len(lines) < 2:
        return None

    l1, l2 = random.sample(lines, 2)

    split1 = re.split(r'[:,\-–]', l1)
    split2 = re.split(r'[:,\-–]', l2)

    part1 = split1[0].strip()
    part2 = split2[-1].strip()


    part1 = " ".join(part1.split()[:7])
    part2 = " ".join(part2.split()[:7])

    part1 = cleanEdgeWords(part1)
    part2 = cleanEdgeWords(part2)

    if len(part1.split()) < 3 or len(part2.split()) < 3:
        return None

    connector = random.choice([
        ",",
        ";",
    ])

    return f"{part1}{connector} {part2}"


def removeBadConnectors(text):
    return re.sub(r'\b(enquanto|após)\b', '', text, flags=re.IGNORECASE)

def ensureStrongEnding(title):
    if not title:
        return title

    weak_words = [
        "de", "do", "da", "dos", "das",
        "para", "pra", "pro",
        "com", "sem",
        "em", "no", "na", "nos", "nas",
        "por", "sobre",
        "e", "ou", "mas",
        "o", "a", "os", "as", "um", "uma"
    ]

    words = title.strip().split()

    if not words:
        return title

    last = words[-1].lower()


    if last in weak_words:
        words.pop()


    if len(words) < 3:
        return " ".join(words)


    if re.match(r'^[^a-zA-ZÀ-ÿ]+$', words[-1]):
        words.pop()


    if random.random() < 0.25:
        endings = [
            "entenda",
            "veja detalhes",
            "diz especialista",
            "segundo analistas",
            "e repercute",
            "e gera reação",
            "mercado reage",
            "mas a que custo?"
        ]

        # só adiciona se já não parecer completo
        if words[-1].lower() not in ["reação", "detalhes", "especialista"]:
            words.append(random.choice(endings))

    return " ".join(words)

def removeBrokenComparisons(text):
    fixes = [

        (r'\b(do que)\s*,', ''),


        (r'\bmais do que\s*$', ''),

        (r'\bdo que\s*$', ''),
    ]

    for pattern, repl in fixes:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    return text.strip()


def cleanEdgeWords(text):
    return re.sub(
        r'\b(e|ou|mas|porém|porque|que)\s*$',
        '',
        text,
        flags=re.IGNORECASE
    ).strip()
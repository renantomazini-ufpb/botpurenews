import feedparser
import random
from pathlib import Path

def loadRSSList(path):
    feeds = {}

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            category, url = line.split("|", 1)

            if category not in feeds:
                feeds[category] = []

            feeds[category].append(url)

    return feeds

def getNews():
    base_dir = Path(__file__).resolve().parent
    rss_path = base_dir.parent / "fontsNews" / "news_PTBR.txt"

    rss_list = loadRSSList(rss_path)
    if not rss_list:
        return []

    urls = []

    for category in rss_list:
        urls.append(random.choice(rss_list[category]))

    random.shuffle(urls)
    urls = urls[:4]

    feeds_entries = []

    for url in urls:
        feed = feedparser.parse(url)
        entries = [e.title for e in feed.entries if hasattr(e, "title")]
        random.shuffle(entries)
        feeds_entries.append(entries[:8])  # até 8 por feed

    # 🔥 mistura intercalando
    mixed = []
    for i in range(8):
        for feed in feeds_entries:
            if i < len(feed):
                mixed.append(feed[i])

    # remove duplicados mantendo ordem
    seen = set()
    final = []
    for t in mixed:
        if t not in seen:
            seen.add(t)
            final.append(t)

    return final[:32]

'''
def getNews():
    titlesNews = []

    base_dir = Path(__file__).resolve().parent
    rss_path = base_dir.parent / "fontsNews" / "news_PTBR.txt"

    rss_list = loadRSSList(rss_path)

    if not rss_list:
        return []

    urls = random.sample(rss_list, k=min(4, len(rss_list))) #ao invés do choice, usarei o sample, evitar duplicatas
    #print("Feeds selecionados:") #colocando por controle por enquanto
    #for url in urls:
    #    print(url)

    for url in urls:
        feed = feedparser.parse(url)
        entries = [e.title for e in feed.entries if hasattr(e, "title")]
        
        sample = random.sample(entries, k=min(8, len(entries)))
        titlesNews.extend(sample)

    titlesNews = list(set(titlesNews))
    random.shuffle(titlesNews)  

    return titlesNews[:32]'''

def getVideo():
    titlesNews = []

    base_dir = Path(__file__).resolve().parent
    rss_path = base_dir.parent / "fontsNews" / "videos_PTBR.txt"

    rss_list = loadRSSList(rss_path)

    if not rss_list:
        return []

    urls = random.sample(rss_list, k=min(4, len(rss_list))) #ao invés do choice, usarei o sample, evitar duplicatas
    #print("Feeds selecionados:") #colocando por controle por enquanto
    #for url in urls:
    #    print(url)

    for url in urls:
        feed = feedparser.parse(url)
        entries = [e.title for e in feed.entries if hasattr(e, "title")]
        
        sample = random.sample(entries, k=min(8, len(entries)))
        titlesNews.extend(sample)

    seen = set()
    titlesNews = [t for t in titlesNews if not (t in seen or seen.add(t))]
    random.shuffle(titlesNews)  

    return titlesNews[:32]






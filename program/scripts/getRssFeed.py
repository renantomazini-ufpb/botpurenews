import feedparser
import random
from pathlib import Path

def loadRSSList(path): #pegar a lista lá
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

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

    return titlesNews[:32]






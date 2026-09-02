import feedparser
import random
import http.client
import urllib.request
import html  # Adicionado para limpar HTML entities (&quot;, &#39;)
from pathlib import Path
import requests

def loadRSSList(path):
    feeds = {}
    if not path.exists():
        print(f"Aviso: Arquivo {path} não encontrado.")
        return feeds

    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Ignores linhas vazias ou comentários
            if not line or line.startswith('#'):
                continue
            
            # Valida se a linha realmente contém o separador '|'
            if '|' not in line:
                print(f"Aviso: Linha {line_num} ignorada por falta do separador '|': '{line}'")
                continue

            category, url = line.split("|", 1)
            category = category.strip()
            url = url.strip()

            if category not in feeds:
                feeds[category] = []
            feeds[category].append(url)

    return feeds



def fetch_feed_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text

'''def fetch_feed_content(url):

    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read()

        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            return content.decode('iso-8859-1', errors='replace')'''

def extract_titles(url):

    content = fetch_feed_content(url)
    feed = feedparser.parse(content)
    
    if not getattr(feed, "entries", None):
        return []

    titles = []
    for e in feed.entries:
        if hasattr(e, "title") and e.title:
            # html.unescape converte &quot; para " e &#39; para '
            clean_title = html.unescape(e.title.strip())
            titles.append(clean_title)
            
    return titles

def getNews():
    base_dir = Path(__file__).resolve().parent
    rss_path = base_dir.parent / "fontsNews" / "news_PTBR.txt"

    rss_list = loadRSSList(rss_path)
    if not rss_list:
        return []

    # Sorteia 1 URL de cada categoria para garantir diversidade
    urls = [random.choice(rss_list[cat]) for cat in rss_list]
    random.shuffle(urls)
    urls = urls[:4]

    feeds_entries = []

    for url in urls:
        try:
            entries = extract_titles(url)
            if entries:
                random.shuffle(entries)
                feeds_entries.append(entries[:8])
        except Exception as e:
            print(f"Aviso: falha ao carregar {url} ({e}). Pulando...")
            continue

    # Intercala as notícias dos diferentes feeds
    mixed = []
    for i in range(8):
        for feed in feeds_entries:
            if i < len(feed):
                mixed.append(feed[i])

    # Remove duplicatas mantendo a ordem
    seen = set()
    return [t for t in mixed if not (t in seen or seen.add(t))][:32]

def getVideo():
    base_dir = Path(__file__).resolve().parent
    rss_path = base_dir.parent / "fontsNews" / "videos_PTBR.txt"

    rss_list = loadRSSList(rss_path)
    if not rss_list:
        return []

    # Pega até 4 feeds aleatórios
    all_urls = [url for urls in rss_list.values() for url in urls]
    urls = random.sample(all_urls, k=min(4, len(all_urls)))

    titlesNews = []

    for url in urls:
        try:
            entries = extract_titles(url)
            sample = random.sample(entries, k=min(8, len(entries)))
            titlesNews.extend(sample)
        except Exception as e:
            print(f"Aviso: falha ao carregar vídeo {url} ({e}). Pulando...")
            continue

    seen = set()
    final_titles = [t for t in titlesNews if not (t in seen or seen.add(t))]
    random.shuffle(final_titles)

    return final_titles[:32]
import feedparser
import time
import socket

socket.setdefaulttimeout(10)  # timeout global

urls = [
    # G1 (rápidos e estáveis)
    "https://g1.globo.com/dynamo/rss2.xml",
    "https://g1.globo.com/dynamo/economia/rss2.xml",
    "https://g1.globo.com/dynamo/mundo/rss2.xml",
    "https://g1.globo.com/dynamo/tecnologia/rss2.xml",
    "https://g1.globo.com/dynamo/carros/rss2.xml",
    "https://g1.globo.com/rss/g1/pop-arte/",
    "https://ge.globo.com/Esportes/Rss/0,,AS0-9645,00.xml",

    # UOL
    "https://rss.uol.com.br/feed/cinema.xml",
    "https://rss.uol.com.br/feed/tecnologia.xml",
    "https://rss.uol.com.br/feed/jogos.xml",

    # Folha
    "https://feeds.folha.uol.com.br/opiniao/rss091.xml",
    "https://feeds.folha.uol.com.br/esporte/rss091.xml",
    "https://feeds.folha.uol.com.br/poder/rss091.xml",
    "https://feeds.folha.uol.com.br/mundo/rss091.xml",
    "https://feeds.folha.uol.com.br/tec/rss091.xml",

    # Tech / mídia
    "https://rss.tecmundo.com.br/feed",
    "https://canaltech.com.br/rss/",
    "https://manualdousuario.net/feed/",

    # Economia / negócios
    "https://www.infomoney.com.br/feed/",

    # Ciência / institucional
    "https://portal.fiocruz.br/rss.xml",
    "https://agencia.fapesp.br/rss",
    "https://www.ufrgs.br/ufrgs/noticias/feed",

    # Cultura / opinião
    "https://piaui.uol.com.br/feed/",
    "https://ojoioeotrigo.com.br/feed/",
    "https://revistaforum.com.br/feed",

    # Outros razoáveis
    "https://www.gazetadopovo.com.br/feed/rss/ultimas-noticias.xml",
    "https://www.gazetadopovo.com.br/feed/rss/cultura.xml",
    "https://www.gazetadopovo.com.br/feed/rss/tudo-sobre/big-techs.xml",

    # Governo (ok, mas às vezes lento)
    "https://www.camara.leg.br/noticias/rss/ultimas-noticias",

    # Esportes
    "https://www.gazetaesportiva.com/futebol/futebol-internacional/feed/",
    "https://www.gazetaesportiva.com/times/brasil/feed/",
    "https://www.ogol.com.br/rss/noticias.php",

    # Regional / menor (menos confiável, mas variado)
    "https://metropoleonline.com.br/rss/latest-posts",
    "https://feeds.feedburner.com/asbeiras"
]

def test_feed(url):
    start = time.time()
    try:
        feed = feedparser.parse(url)
        elapsed = time.time() - start

        if feed.bozo:
            return (url, "erro parsing", round(elapsed, 2))

        if not feed.entries:
            return (url, "sem entradas", round(elapsed, 2))

        return (url, "ok", round(elapsed, 2))

    except Exception as e:
        return (url, f"erro: {type(e).__name__}", None)


results = [test_feed(url) for url in urls]

# ordena pelos mais lentos
results.sort(key=lambda x: (x[2] is None, x[2] or 999))

for r in results:
    print(r)
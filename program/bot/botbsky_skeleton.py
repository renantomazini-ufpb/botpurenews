from atproto import Client
from program.scripts import geradorNew
import time
import os

client = Client()

# pegar do ambiente (GitHub Actions vai fornecer)
user = os.environ.get("BSKY_USER")
password = os.environ.get("BSKY_PASS")

if not user or not password:
    raise ValueError("Credenciais não encontradas")

client.login(user, password)


def post():
    news = geradorNew.getANews()
    print("Postando:", news)

    try:
        client.send_post(news[:300])  # limite Bluesky
    except Exception as e:
        print("Erro ao postar:", e)


# loop (pra rodar localmente)
if __name__ == "__main__":
    while True:
        post()
        time.sleep(3600)
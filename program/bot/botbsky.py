from atproto import Client
from program.scripts import geradorNew
import time
import os

client = Client()

# GitHub actions aqui
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


# ... (seus imports e definições de função permanecem iguais)


if __name__ == "__main__":
    try:
        post()
        print("Execução finalizada com sucesso.")
    except Exception as error:
        print(f"Falha na execução agendada: {error}")
        exit(1) # Avisa o GitHub que algo deu errado
    #conflito com actions!
    #while True:
    #    post()
    #    time.sleep(3600)
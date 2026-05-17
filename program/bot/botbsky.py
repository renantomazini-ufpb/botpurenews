from atproto import Client
from program.scripts import geradorNew
import time
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Inicialize o cliente passando os cabeçalhos customizados
client = Client()
client.request.headers.update(HEADERS) # <-- Força a biblioteca a se disfarçar de navegador

# O resto do seu código continua exatamente igual...
user = os.environ.get("BSKY_USER")
password = os.environ.get("BSKY_PASS")
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
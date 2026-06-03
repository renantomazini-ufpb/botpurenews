from pathlib import Path
import sys
import os


scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from maybeAcusation import maybeAcusation


def buildAcusationPost():
    return maybeAcusation()


def postAcusation():
    from atproto import Client

    client = Client()

    user = os.environ.get("BSKY_USER")
    password = os.environ.get("BSKY_PASS")

    if not user or not password:
        raise ValueError("Credenciais nao encontradas")

    client.login(user, password)

    acusation = buildAcusationPost()
    print("Postando acusacao:", acusation)

    try:
        client.send_post(acusation[:300])  # limite Bluesky
    except Exception as e:
        print("Erro ao postar acusacao:", e)


if __name__ == "__main__":
    try:
        postAcusation()
        print("Acusacao postada com sucesso.")
    except Exception as error:
        print(f"Erro no bot de acusacoes: {error}")
        exit(1)

from pathlib import Path
import random


base_dir = Path(__file__).resolve().parent
words_dir = base_dir.parent / "wordsData"
multador_dir = base_dir.parent / "multador"


def loadList(path):
    with open(path, "r", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]


def loadAcusationWords():
    return {
        "chars": loadList(words_dir / "saltWordsChars_PTBR.txt"),
        "infracoes": loadList(multador_dir / "infracoes.txt"),
    }


def maybeAcusation():
    words = loadAcusationWords()
    char = random.choice(words["chars"])
    infracao = random.choice(words["infracoes"])

    connectives = [
        "foi multado por",
        "recebe multa por",
        "leva multa por",
        "vai responder por",
        "foi cancelado por",
        "responde por",
        "entra na mira por",
        "vira alvo por",
        "foi acusado de",
        "foi denunciado por",
        "foi processado por",
    ]

    return f"Atenção: {char} {random.choice(connectives)} {infracao}"

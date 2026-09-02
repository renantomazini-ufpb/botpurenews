from jornalistChefEstagiario import *
from maybeAcusation import maybeAcusation



def PrintNews(n):
    print("printando news")
    for x in range(n):
        print(getOneNews())

def getANews():
    print("pegando news")
    return getOneNews()

def PrintMaybeAcusation(n):
    print("printando acusacoes")
    for x in range(n):
        print(maybeAcusation())

'''def PrintVideos(n):
    print("printando videos")
    for x in range(n):
        print(retornaVideo())'''


PrintNews(5)
#PrintMaybeAcusation(5)
#PrintVideos(1)

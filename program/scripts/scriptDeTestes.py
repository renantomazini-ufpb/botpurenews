from jornalistChefEstagiario import *



def PrintNews(n):
    print("printando news")
    for x in range(n):
        print(getOneNews())

def getANews():
    print("pegando news")
    return getOneNews()

def PrintVideos(n):
    print("printando videos")
    for x in range(n):
        print(retornaVideo())


PrintNews(5)
#PrintVideos(1)
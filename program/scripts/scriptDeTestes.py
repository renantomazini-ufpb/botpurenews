from jornalistChefEstagiario import *



def PrintNews(n):
    print("printando news")
    for x in range(n):
        print(getOneNews())

def getANews():
    print("pegando news")
    return getOneNews()


PrintNews(4)
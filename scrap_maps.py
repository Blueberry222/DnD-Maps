import praw
import pandas as pd
import urllib.request
from urllib.error import HTTPError
import csv
import time
from datetime import datetime

def url_to_jpg(i, url, mapas_diretório):
    # i: numero da imagem. url: URL da imagem. mapas_diretório: Diretório final das imagens.
    if url.endswith(".jpg") or url.endswith(".png"):
        hoje = datetime.now()
        nome_do_arquivo = "{}-mapa.jpg".format(hoje.strftime("%d-%m-%Y, %H-%M-%S"))
        diretório_final = "{}/{}".format(mapas_diretório, nome_do_arquivo)
        urllib.request.urlretrieve(url, diretório_final)
        print("{} salvo".format(nome_do_arquivo))
    else:
        return None

reddit = praw.Reddit(client_id='idreddit', \
                     client_secret='secretreddit', \
                     user_agent='nomedoagent', \
                     username='seuusername', \
                     password='suasenha') # Permite abrir o reddit com suas credenciais. Acesse https://github.com/reddit-archive/reddit/wiki/OAuth2

subreddit = reddit.subreddit('dndmaps') # Especifica o subreddit

hot_subreddit = subreddit.hot(limit=250) # Filtra por "HOT"

topics_dict = {"url":[]} #"title":[] dicionário URL

mapas = "MAPAS.csv"
mapas_diretório = "E:\Downloads\RPG\Mapas"

for post in hot_subreddit:
    # topics_dict["title"].append(post.title)
    topics_dict["url"].append(post.url) # Append a url pro dict

# Cria CSV
topics_data = pd.DataFrame(topics_dict)
topics_data.to_csv('MAPAS.csv', index=False) 

# Lê listas de URLS com o Panda Dataframe
urls = pd.read_csv(mapas)

# Salva imagens no diretório iterando em uma lista

for i, url, in enumerate(urls.values):
        try:
            url_to_jpg(i, url[0], mapas_diretório)
            time.sleep(1)
        except HTTPError as e:
            print(e)
            time.sleep(10)
            continue

from bs4 import BeautifulSoup
import requests 
import re
import json
from unicodedata import normalize

def get_ted_website_publication(url):
    if "ted" not in str(url):
        raise Exception("Url Invalida")

    response = requests.get(url)

    soup = BeautifulSoup(response.content,"html.parser")
    textbody = soup("div", {"class":"Grid Grid--with-gutter d:f@md p-b:4"})
    texts = []

    for div in textbody:
        text = div("p")[0].text
        text = text.strip()
        text = text.replace("\n"," ")
        text = text.replace("\t"," ")
        text = re.sub(' +',' ', text)
        texts.append(text)
    
    texttitle = soup.title.text
    author = texttitle.split(":")[0].strip()
    title = texttitle.split(":")[1].split("|")[0].strip()

    finaljson = {
        "author": author,
        "body": " ".join(texts),
        "title": title,
        "type": "video",
        "url": url
    }

    return finaljson

def get_olhardigital_website_publication(url):
    if "olhardigital" not in str(url):
        raise Exception("Url Invalida")

    response = requests.get(url)

    soup = BeautifulSoup(response.content,"html.parser")
    textbody = soup("article",{"class":"mat-container"})[0]("div",{"class":"mat-txt"})
    texts = []

    for divs in textbody:
        div = divs("p")
        for p in div:
            text = p.text
            text = text.strip()
            text = text.replace("\n"," ")
            text = text.replace("\t"," ")
            text = re.sub(' +',' ', text)
            texts.append(text)
    
    author = soup("span",{"class":"meta-item meta-aut"})[0].text
    title = soup("h1", {"class":"mat-tit"})[0].text

    finaljson = {
        "author": author,
        "body": " ".join(texts),
        "title": title,
        "type": "article",
        "url":url
    }

    return finaljson

def get_startse_website_publication(url):
    if "startse" not in str(url):
        raise Exception("Url Invalida")

    response = requests.get(url)
    
    soup = BeautifulSoup(response.content,"html.parser")
    textbody = soup("span",{"style":"font-weight: 400;"})
    texts = []
    
    for span in textbody:
        text = span.text
        text = text.strip()
        text = text.replace("\n"," ")
        text = text.replace("\t"," ")
        text = re.sub(' +',' ', text)
        texts.append(text)
    
    author = soup("div", {"class":"title-single__info"})[0]("h4")[0]("a")[0].text
    title = soup("div", {"class":"title-single__title"})[0]("h2")[0].text

    finaljson = {
        "author": author,
        "body": " ".join(texts),
        "title": title,
        "type": "article",
        "url": url
    }
    return finaljson

def remove_accents(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def savejson(data):
    title = data["title"]
    title = title.replace(" ", "_")
    title = title.replace(".", "")
    title = title.replace(":", "")
    title = remove_accents(title)
  
    with open(title + ".json", 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=0)


urls_ted = ["https://www.ted.com/talks/helen_czerski_the_fascinating_physics_of_everyday_life/transcript?language=pt-br#t-81674",
"https://www.ted.com/talks/kevin_kelly_how_ai_can_bring_on_a_second_industrial_revolution/transcript?language=pt-br",
"https://www.ted.com/talks/sarah_parcak_help_discover_ancient_ruins_before_it_s_too_late/transcript?language=pt-br",
"https://www.ted.com/talks/sylvain_duranton_how_humans_and_ai_can_work_together_to_create_better_businesses/transcript?language=pt-br",
"https://www.ted.com/talks/chieko_asakawa_how_new_technology_helps_blind_people_explore_the_world/transcript?language=pt-br",
"https://www.ted.com/talks/pierre_barreau_how_ai_could_compose_a_personalized_soundtrack_to_your_life/transcript?language=pt-br",
"https://www.ted.com/talks/tom_gruber_how_ai_can_enhance_our_memory_work_and_social_lives/transcript?language=pt-br"]

urls_olhar_digital = ["https://olhardigital.com.br/colunistas/wagner_sanchez/post/o_futuro_cada_vez_mais_perto/78972",
"https://olhardigital.com.br/colunistas/wagner_sanchez/post/os_riscos_do_machine_learning/80584",
"https://olhardigital.com.br/ciencia-e-espaco/noticia/nova-teoria-diz-que-passado-presente-e-futuro-coexistem/97786",
"https://olhardigital.com.br/noticia/inteligencia-artificial-da-ibm-consegue-prever-cancer-de-mama/87030",
"https://olhardigital.com.br/ciencia-e-espaco/noticia/inteligencia-artificial-ajuda-a-nasa-a-projetar-novos-trajes-espaciais/102772",
"https://olhardigital.com.br/colunistas/jorge_vargas_neto/post/como_a_inteligencia_artificial_pode_mudar_o_cenario_de_oferta_de_credito/78999",
"https://olhardigital.com.br/ciencia-e-espaco/noticia/cientistas-criam-programa-poderoso-que-aprimora-deteccao-de-galaxias/100683"]

url_startse = "https://www.startse.com/noticia/startups/mobtech/deep-learning-o-cerebro-dos-carros-autonomos"

for url in urls_olhar_digital:
    data = get_olhardigital_website_publication(url)
    savejson(data)

for url in urls_ted:
    data = get_ted_website_publication(url)
    savejson(data)


data = get_startse_website_publication(url_startse)
savejson(data)
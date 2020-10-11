from requests import get
from time import sleep
from bs4 import BeautifulSoup
from pathlib import Path


def get_articles_from_category(url):
    # returns [[name, href]...]
    page2 = get(url)
    soup2 = BeautifulSoup(page2.text, 'html.parser')
    link_list2 = soup2.select("h3 > a")
    articles = []
    for article in link_list2:
        articles.append([article.contents[0].contents[0],
                         "https://bbc.com" + article.get("href")])
    return articles


# parte dos artigos
def get_html_from_article_href(name, url):
    # gets a article name, article href and returns an html
    print(name)
    article_page = get(url)
    article_soup = BeautifulSoup(article_page.text, 'html.parser')
    inner_body = article_soup.main
    home = str(Path.home())
    filepath = home + "/bbc/" + name + ".html"
    # TODO ver como salvar isso num formato mais ou menos que dê pra
    # ler no kindle, que vá concatenando a saída e monte um índice.
    with open(filepath, "w", encoding='utf-8') as file:
        entries = inner_body.findAll(['h1', 'h2', 'p'])
        # este pop tira o parágrafo com o anúncio do youtube
        entries.pop()
        for entry in entries:
            file.write(str(entry))


page = get('https://www.bbc.com/portuguese')
soup = BeautifulSoup(page.text, 'html.parser')
# parte que pega a página principal
link_list_items = soup.find_all('a')
categories = {"Brasil": "", "Internacional": "",
              "Economia": "",  "Saúde": "",
              "Ciência": "", "Tecnologia": ""}

for category in link_list_items:
    current = category.contents[0]
    if current in categories:
        categories[current] = "https://bbc.com" + category.get("href")

for (category_name, cat_url) in categories.items():
    articles = get_articles_from_category(cat_url)
    for article in articles:
        sleep(6)
        [name, url] = article
        get_html_from_article_href(name, url)
    sleep(10)

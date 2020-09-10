from requests import get
from time import sleep
from bs4 import BeautifulSoup

def get_articles_from_category(url):
    # returns [[name, href]...]
    page2 = get(url)

    soup2 = BeautifulSoup(page2.text, 'html.parser')

    remove_nav_bar = soup2.find("ul")
    remove_nav_bar.decompose()

    link_list2 = soup2.select("h3 > a")

    articles = []

    for article in link_list2:
        articles.append([article.contents[0].contents[0], "https://bbc.com" + article.get("href")])

    return articles

# parte dos artigos
def get_html_from_article_href(name, url):
    # gets a article name, article href and returns an html
    print(name)
    article_page = get(url)
    article_soup = BeautifulSoup(article_page.text, 'html.parser')
    social_media = article_soup.find(class_='with-extracted-share-icons')
    if social_media:
        social_media.decompose()
    inner_body = article_soup.find(class_="story-body__inner")
    if inner_body:
        scripts = inner_body.findAll(['script', 'style', 'svg'])
    else:
        return 0
    if scripts:
        for script in scripts:
            script.decompose()
    extra_elements = inner_body.findAll(class_=[
        'tags-title',
        'share__title',
        'group__title',
        'navigation--footer__heading',
        'orb-footer-lead',
        'navigation__heading',
        'off-screen'
    ])
    for item in extra_elements:
        item.decompose()
    filename = name
            # TODO ver como salvar isso num formato mais ou menos que dê pra ler
            # no kindle, que vá concatenando a saída e monte um índice.
    with open("/home/sean/bbc/" + filename + ".html", "w", encoding='utf-8') as file:
        entries = inner_body.findAll(['h1', 'h2', 'p'])
        entries.pop()
        header = article_soup.find(class_='story-body__h1')
        entries.insert(0, header)
        for entry in entries:
            file.write(entry.prettify())

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

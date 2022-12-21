import requests
from bs4 import BeautifulSoup as bs


def getHtml(url):
    return requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36', 'accept': '*/*'})


def getPages(htmlText):
    return int(bs(htmlText, 'html.parser').find('span', class_='navigation').find_all('a')[-1].get_text(strip=True) if bs(htmlText, 'html.parser').find('span', class_='navigation') else 1)


def getContent(htmlText):
    items = bs(htmlText, 'html.parser').find_all('article', class_='short')
    mainInfo = []

    for i in items:
        mainInfo.append({
            'title': i.find('h2').get_text(strip=True),
            'rating': i.find('div', class_='rate_nums').get_text(strip=True)[:-1:],
            'status': i.find('div', class_='short-meta').get_text(strip=True)
        })
    return mainInfo


def parserAnimeFox():
    url = input('put the url: ').strip()
    html = getHtml(url)
    if html.status_code == 200:
        pages = getPages(html.text)
        anime = []

        for page in range(1, pages + 1):
            print(f'parsing {page}/{pages}...', end='\r')
            html = getHtml(url + f"page/{page}")
            anime.extend(getContent(html.text))

        print(f'Done, it`s found {len(anime)} animes')
        print(anime)

        return anime


if __name__ == '__main__':
    parserAnimeFox()

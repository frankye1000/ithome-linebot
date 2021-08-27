import requests
from bs4 import BeautifulSoup
from datetime import date

today = date.today()
today = today.strftime("%Y-%m-%d")


def crawl_ithome():
    re = []
    for p in range(2):

        r = requests.get("https://www.ithome.com.tw/news?page=%s"%p)
        soup = BeautifulSoup(r.text, "html5lib")
        select_item = soup.select('div.item')
        for i in select_item:
            select_title = i.select('p.title')
            select_url = i.select('p.title > a')
            select_day = i.select('p.post-at')
            select_photo = i.select('p.photo > a > img ')

            title = select_title[0].text
            url = 'https://www.ithome.com.tw'+select_url[0].get('href')
            day = select_day[0].text.strip(' ')
            photo = select_photo[0].get('src')

            if day == today:
                re.append((title[:40],url,day,photo))    # title只能40個字
    return re
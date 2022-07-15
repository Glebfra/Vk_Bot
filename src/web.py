import requests
from bs4 import BeautifulSoup


class WebScrap(object):
    def __init__(self, url):
        self.url = url
        self.old_result = {}

    def get_last_new(self):
        result = {}
        try:
            request = requests.get(url=self.url)
            soup = BeautifulSoup(request.content, features='xml')
            articles = soup.find('item')
            for type in ['title', 'link']:
                result[type] = articles.find(type).text
            if result['title'].find('06-012') + 1 or result['title'].find('012') + 1 \
                    or result['title'].find('12') + 1:
                if self.old_result != result:
                    self.old_result = result
                    return result
            else:
                return None
        except:
            return None

    def get_all_news(self):
        pass


if __name__ == '__main__':
    url = 'https://shine.ylsoftware.com/feed/'
    request = requests.get(url)
    soup = BeautifulSoup(request.content, features='xml')
    article = soup.find('item').find('title').text
    print(article)

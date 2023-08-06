import re
from collections import namedtuple
from bs4 import BeautifulSoup

from Downloader.url_request import UrlRequest


class Book:
    def __init__(self, search_book, settings):
        self.settings = settings
        self.search_url = settings.search_url
        self.article_urls = settings.article_urls
        self.book_name = search_book
        UrlRequest.pretend_header(self.settings.request_head_paras_file)
        self.url_request = UrlRequest('utf-8')
        self.book_url = None

    def get_book_info(self):
        data = {'keyword': self.book_name, 't': '1'}
        html = self.url_request.post(data, self.search_url)
        self._parse_book_html(html)

    def _parse_book_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        books = soup.find_all('div', attrs={'class': 'hot_sale'})
        for book in books:
            self.settings.choose_urls.append(self._set_book(str(book)))

    @staticmethod
    def _set_book(html):
        Book = namedtuple('Book', ['id', 'title', 'author'])
        book_id = re.search(r'<a href="(/.*?/)">', html)
        title = re.search(r'<p class="title">(.*?)</p>', html)
        author = re.search(r'<p class="author">.*作者：(.*?)</p>', html)
        return Book(book_id[1], title[1], author[1])

    def make_choice(self,index):
        self.book_url = self.settings.choose_urls[index]

    def get_urls_article(self):
        if not isinstance(self.book_url, tuple):
            raise ValueError('Not choose a book')
        start_url = self.settings.index_url + self.book_url[0]
        html = self.url_request.get(start_url)
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find('div', attrs={'id': 'list'})
        pattern = r'<a href="%s(.*?)">' % (self.book_url[0])
        urls = re.findall(pattern, str(result))
        for i in range(len(urls)):
            self.article_urls.append(start_url + urls[i])

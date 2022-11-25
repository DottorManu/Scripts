#requisites: pip install requests, bs4, natsort

import requests
import urllib.request
import os
from bs4 import BeautifulSoup
from natsort import natsorted
from urllib.parse import urlparse

def get_links(url, filter, pagination):
    link_list = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a')
    base_url = urlparse(url).scheme + '://' + urlparse(url).netloc
    for link in links:
        if filter in link['href']:
            link_list.append(base_url + link['href'])
    if(pagination):
        number_of_books = int(page.text.split('Number of books: ')[1].split('<br>')[0])
        offset = 25
        while offset < number_of_books:
            link_list.extend(get_links(url + '&limit=25&offset=' + str(offset), filter, False))
            offset = offset + 25
    return link_list

def download_file(url, path):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': "application/pdf",
    'Referer': url.replace('getBook','book'),
    'Accept': 'application/pdf'
    }

    cookies = {'PHPSESSID': 'ba6b0a36-7370-44ed-b026-1edecedb4987'}
    response = requests.get(url, allow_redirects=True, cookies=cookies, headers=headers)
    if 'Content-disposition' in response.headers:
        filename = (response.headers['Content-disposition'].split('filename=')[1].replace(':',' -').replace('?','').replace('/', ' - '))[1: -1]
        open(os.path.join(path, filename), 'wb').write(response.content)
        print("Dumping: " + url.split('id=')[1] + " - " + filename)

topic_list, book_list, link_list = [], [], []

#retrive all book links
topic_list = get_links("http://51.195.220.149/", 'topic.php?id=', False)
for topic in topic_list: book_list.extend(get_links(topic,'book.php?id=', True))
link_list = natsorted([(lambda book: book.replace('book', 'getBook'))(book) for book in book_list])

#download all books from links
for link in link_list: download_file(link, 'libri/')

#Alternative: all links are the same, with "id" going from 1 to 1165, here's a fast way to generate them and get all books
#for i in range(1, 1166): download_file('http://51.195.220.149/getBook.php?id=' + str(i), 'books/')

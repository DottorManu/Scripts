import requests
import urllib.request
import os
from bs4 import BeautifulSoup
from natsort import natsorted
from urllib.parse import urlparse

saved_files = []

def get_fixed_path(url, text):
    file_extension = get_extension(text, url.split('/')[-1])
    path = url.replace(':', '_').replace('?', '-') + file_extension
    return path

def get_extension(text, name):
    ext = ''
    if is_html(text):
        if '.html' not in name:
            ext = '.html'
    return ext

def is_html(text):
    if 'doctype html' in text.lower():
        return True
    else:
        return False

def save_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(content)

def save_html(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wt', encoding="UTF-8").write(text)

def get_all_internal_links(text):
    soup = BeautifulSoup(text, 'html.parser')
    link_raccolti = []
    link_finali = {}
    for tag in (soup.find_all('a', {'href': True}) + soup.find_all('link', {'href': True})): link_raccolti.append(tag['href'])
    for tag in soup.find_all('script', {'src': True}): link_raccolti.append(tag['src'])
    for link in link_raccolti:
        if (len(link) > 1) and (('/'+link.split('/')[-1]+'/') not in starting_url):
            if(link[0] == '/'):
                link_finali[base_url + link.replace('//', '/')] = ''
            else:
                if(':' in link and '.' in link):
                    site = urlparse(link).netloc.split(':')[0]
                    site = site.split('.')[-2] + '.' + site.split('.')[-1]
                    if site in base_url:
                        link_finali[link] = ''
    return list(link_finali)

def download(url, depth):
    global base_path
    global saved_files
    global max_depth
    
    if depth > max_depth:
        return url

    page = requests.get(url)
    file_path = os.path.join(base_path, get_fixed_path(url, page.text))

    if url in saved_files:
        return file_path
    
    print(('  ' * (depth-1))+url)
    saved_files.append(url)
    
    if is_html(page.text):
        links = get_all_internal_links(page.text)
        links.reverse()
        html_page = page.text
        if url in links: links.remove(url)
        for link in links:
            temp_file_path = download(link, depth +1)
            html_page = html_page.replace(link, r'file:///' + temp_file_path)
        save_html(file_path, html_page)
    else:
        save_file(file_path, page.content)
    return file_path

def start_dumper(url, path):
    global base_url
    base_url = urlparse(url).scheme + '://' + urlparse(url).netloc
    global starting_url
    starting_url = url
    global base_path
    base_path = path
    global max_depth
    max_depth = 3
    download(url, 1)

    
start_dumper(r'https://www.bmw-etk.info/catalogo-dei-ricambi/cat/Mini/VT/P/R56/Cou/Cooper%20D/ECE/L/N/2008/07/51501', r"C:\Users\MattDC\Desktop\Sito sceso")

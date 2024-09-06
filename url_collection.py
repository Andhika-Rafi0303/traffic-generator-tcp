import requests
from bs4 import BeautifulSoup
import csv

def get_all_urls(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    urls = set()
    for link in soup.find_all('a', href=True):
        url = link['href']
        if url.startswith('/'):
            url = base_url + url
        urls.add(url)
    
    return urls

base_url = 'https://www.detik.com'
all_urls = get_all_urls(base_url)


with open('urls_detik.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['URL'])  
    
    for url in all_urls:
        csvwriter.writerow([url])

print(f"Jumlah konten yang ditemukan: {len(all_urls)}")

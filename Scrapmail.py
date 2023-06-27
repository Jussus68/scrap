import requests
from bs4 import BeautifulSoup
import re
import csv
from urllib.parse import urljoin

urls = ["https://max-powerlifting.fr/"]  # Remplacez par les URLs des sites que vous avez l'autorisation de scraper

regex = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"  # se faire passer pour Googlebot
}

visited = set()

def crawl(url):
    if url in visited:
        return

    visited.add(url)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver les emails sur la page
    emails = re.findall(regex, str(soup))
    for email in emails:
        first_name = email.split('@')[0]
        writer.writerow([first_name, email])

    # Trouver tous les liens sur la page
    for link in soup.find_all('a'):
        page_url = link.get('href')
        # Assurez-vous que le lien est valide
        if page_url and not page_url.startswith('#'):
            page_url = urljoin(url, page_url)
            # Appeler récursivement la fonction crawl sur la nouvelle URL
            crawl(page_url)

with open('emails.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["FirstName", "Email"])
    
    for url in urls:
        visited = set()  # Réinitialiser l'ensemble des URLs visitées pour chaque nouvelle URL de base
        crawl(url)

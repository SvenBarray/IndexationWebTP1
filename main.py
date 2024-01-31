import time
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup

def crawl(start_url, max_urls=50):
    visited_urls = set()
    urls_to_visit = [start_url]

    while urls_to_visit and len(visited_urls) < max_urls:
        current_url = urls_to_visit.pop(0)
        domain = urljoin(current_url, '/')
        
        try:
            wait_time = _should_wait(domain)
            if wait_time > 0:
                time.sleep(wait_time)

            response = urlopen(current_url) # Effectue la requête HTTP pour obtenir la page
            last_request_time[domain] = datetime.now()  # Mise à jour du temps de la dernière requête
            page_content = response.read()

            soup = BeautifulSoup(page_content, 'html.parser') # Analyse le HTML de la page

            link_count = 0  # Compteur pour le nombre de liens suivis sur la page actuelle
            for link in soup.find_all('a'): # Parcourt tous les liens (<a href="...">) trouvés dans la page
                if link_count >= 5:  # Limite à 5 liens par page
                    break

                href = link.get('href')
                if href and href.startswith('http'):
                    absolute_url = urljoin(current_url, href) # Construit l'URL absolue
                    if absolute_url not in visited_urls and _can_fetch(absolute_url):
                        visited_urls.add(absolute_url)
                        urls_to_visit.append(absolute_url)
                        link_count += 1

            print(f"Crawled: {current_url}")
            time.sleep(5) # Attend 5 secondes pour respecter la règle de politesse

        except Exception as e:
            print(f"Error crawling {current_url}: {e}")
            continue

    return visited_urls

last_request_time = {}  # Dictionnaire pour suivre le temps de la dernière requête par domaine

def _should_wait(domain): # Vérifie si le crawler doit attendre avant de faire une nouvelle requête au domaine donné.
    if domain in last_request_time:
        elapsed = (datetime.now() - last_request_time[domain]).total_seconds()
        if elapsed < 5:
            return 5 - elapsed
    return 0

robot_parsers = {} # Initialisation du dictionnaire pour la mise en cache des parseurs de robots.txt

def _can_fetch(url, user_agent='*'): # Vérifie si le robots.txt du site autorise le crawling
    domain = urljoin(url, '/')
    if domain not in robot_parsers:
        parser = RobotFileParser()
        parser.set_url(urljoin(domain, '/robots.txt'))
        parser.read()
        robot_parsers[domain] = parser
    return robot_parsers[domain].can_fetch(user_agent, url)


if __name__ == "__main__":
    start_url = "https://ensai.fr/"
    crawled_urls = crawl(start_url)
    print("\nCrawled URLs:")
    for url in crawled_urls:
        print(url)

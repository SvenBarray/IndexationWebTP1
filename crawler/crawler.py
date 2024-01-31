import time
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from urllib.error import HTTPError, URLError

from crawler.helpers import fetch_sitemap_urls, can_fetch
from database.modify_database import insert_or_update_page

def crawl(start_url, max_total_urls=50, max_link_count_per_page = 5, courtesy_time = 5):
    "Fonction qui permet de crawler le web en partant d'une page initiale"
    visited_urls = set()
    urls_to_visit = fetch_sitemap_urls(start_url) + [start_url]
    last_request_time = {}  # Dictionnaire pour suivre le temps de la dernière requête par domaine
    robot_parsers = {} # Dictionnaire pour la mise en cache des parseurs de robots.txt

    while urls_to_visit and len(visited_urls) < max_total_urls:
        current_url = urls_to_visit.pop(0)
        domain = urljoin(current_url, '/')

        # Calcul du temps d'attente nécessaire
        if domain in last_request_time: # Cette condition permet de ne pas à avoir à attendre les 'courtesy_time' secondes de politesse si on a changé de domaine
            elapsed_since_last_request = (datetime.now() - last_request_time[domain]).total_seconds()
            if elapsed_since_last_request < courtesy_time:
                time.sleep(courtesy_time - elapsed_since_last_request)

        try:
            with urlopen(current_url) as response:  # Effectue la requête HTTP pour obtenir la page
                page_content = response.read()

            last_request_time[domain] = datetime.now()  # Mise à jour après la requête

            soup = BeautifulSoup(page_content, 'html.parser')  # Analyse le HTML de la page
            link_count = 0  # Compteur pour le nombre de liens suivis sur la page actuelle

            insert_or_update_page(current_url, datetime.now())

            for link in soup.find_all('a'): # Parcourt tous les liens (<a href="...">) trouvés dans la page
                if link_count >= max_link_count_per_page or len(visited_urls) >= max_total_urls:  # Limite à 'max_link_count_per_page' liens par page, et vérifie encore la limite max_urls, pour éviter par exemple de passer de 48 à 53 urls ici avec une limite de 50 urls totaux et 5 liens par page.
                    break

                href = link.get('href')
                if href and href.startswith('http'):
                    absolute_url = urljoin(current_url, href) # Construit l'URL absolue
                    if absolute_url not in visited_urls and can_fetch(absolute_url, robot_parsers):
                        visited_urls.add(absolute_url)
                        urls_to_visit.append(absolute_url)
                        link_count += 1

            print(f"Crawled: {current_url}")

        except HTTPError as e:
            print(f"Erreur HTTP lors de l'accès à {current_url}: {e.code} - {e.reason}")
        except URLError as e:
            print(f"Erreur d'URL lors de l'accès à {current_url}: {e.reason}")
        except ConnectionResetError as e:
            print(f"Connexion réinitialisée par le serveur pour {current_url}: {e}")
            time.sleep(10)  # Pause avant de réessayer
            continue
        except Exception as e:
            print(f"Erreur générale lors de l'accès à {current_url}: {e}")
    
    with open('database/crawled_webpages.txt', 'w') as file: # Écriture des URLs dans un fichier crawled_webpages.txt
        for url in visited_urls:
            file.write(url + '\n')

    return visited_urls
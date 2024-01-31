import threading
from queue import Queue
from urllib.parse import urljoin
from datetime import datetime
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from crawler.helpers import fetch_sitemap_urls, can_fetch
from database.modify_database import insert_or_update_page

def crawl_thread(url_queue, visited_urls, last_request_time, robot_parsers, lock, max_total_urls, max_link_count_per_page, courtesy_time):
    """Fonction pour traiter des URLs dans la file d'attente"""
    while not url_queue.empty() and len(visited_urls) < max_total_urls:
        current_url = url_queue.get()
        domain = urljoin(current_url, '/')

        with lock: # Gestion de la concurrence pour les ressources partagées
            # Attendre pour respecter le temps de courtoisie si nécessaire
            if len(visited_urls) >= max_total_urls:
                break
            if domain in last_request_time:
                elapsed = (datetime.now() - last_request_time[domain]).total_seconds()
                if elapsed < courtesy_time:
                    time.sleep(courtesy_time - elapsed)
            last_request_time[domain] = datetime.now()

        try:
            with urlopen(current_url) as response:
                page_content = response.read()
            soup = BeautifulSoup(page_content, 'html.parser')

            with lock: # Enregistrement et affichage de l'URL traitée
                insert_or_update_page(current_url, datetime.now())
                print(f"Crawled: {current_url}")

            link_count = 0
            for link in soup.find_all('a'):
                if link_count >= max_link_count_per_page:
                    break

                href = link.get('href')
                if href and href.startswith('http'):
                    absolute_url = urljoin(current_url, href)
                    with lock:
                        if absolute_url not in visited_urls and can_fetch(absolute_url, robot_parsers):
                            visited_urls.add(absolute_url)
                            url_queue.put(absolute_url)
                            link_count += 1

        except HTTPError as e:
            print(f"Erreur HTTP lors de l'accès à {current_url}: {e.code} - {e.reason}")
        except URLError as e:
            print(f"Erreur d'URL lors de l'accès à {current_url}: {e.reason}")
        except ConnectionResetError as e:
            print(f"Connexion réinitialisée par le serveur pour {current_url}: {e}")
            time.sleep(10)  # Pause avant de réessayer
        except Exception as e:
            print(f"Erreur générale lors de l'accès à {current_url}: {e}")

def multithreaded_crawl(start_url, max_total_urls=50, max_link_count_per_page=5, courtesy_time=5, num_threads=5):
    """Fonction qui initialise les ressources pour le multithreading"""
    visited_urls = set()
    urls_to_visit = fetch_sitemap_urls(start_url) + [start_url]
    url_queue = Queue()
    for url in urls_to_visit:
        url_queue.put(url)

    last_request_time = {}
    robot_parsers = {}
    lock = threading.Lock() # Verrou pour gérer l'accès concurrent aux ressources partagées

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=crawl_thread, args=(url_queue, visited_urls, last_request_time, robot_parsers, lock, max_total_urls, max_link_count_per_page, courtesy_time)) # Création d'un thread qui exécute la fonction 'crawl_thread'
        t.start() # Démarrage du thread
        threads.append(t)

    for t in threads:
        t.join()

    return visited_urls

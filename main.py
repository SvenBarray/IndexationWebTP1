import time
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def crawl(start_url, max_urls=50):
    visited_urls = set()
    urls_to_visit = [start_url]

    while urls_to_visit and len(visited_urls) < max_urls:
        current_url = urls_to_visit.pop(0)
        try:
            # Effectue la requête HTTP pour obtenir la page
            response = urlopen(current_url) 
            page_content = response.read()

            soup = BeautifulSoup(page_content, 'html.parser') # Analyse le HTML de la page
            for link in soup.find_all('a'): # Parcourt tous les liens (<a href="...">) trouvés dans la page
                href = link.get('href')
                if href and href.startswith('http'):
                    absolute_url = urljoin(current_url, href) # Construit l'URL absolue
                    if absolute_url not in visited_urls:
                        visited_urls.add(absolute_url)
                        urls_to_visit.append(absolute_url)
            
            print(f"Crawled: {current_url}")
            time.sleep(5) # Attend 5 secondes pour respecter la règle de politesse

        except Exception as e:
            print(f"Error crawling {current_url}: {e}")

    return visited_urls

if __name__ == "__main__":
    start_url = "https://ensai.fr/"
    crawled_urls = crawl(start_url)
    print("\nCrawled URLs:")
    for url in crawled_urls:
        print(url)

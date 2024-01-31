from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET
import warnings

def fetch_sitemap_urls(url):
    "Parcours le sitemap et récupère les URL à visiter"
    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
    sitemap_url = urljoin(url, '/sitemap.xml')
    try:
        response = urlopen(sitemap_url)
        sitemap_content = response.read()
        sitemap = ET.fromstring(sitemap_content)
        urls = [loc.text for loc in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        return urls
    except Exception as e:
        print(f"Erreur lors de la récupération du sitemap : {e}")
        return []

def can_fetch(url, robot_parsers, user_agent='*'):
    """Vérifie si le robots.txt du site autorise le crawling"""
    domain = urljoin(url, '/')
    if domain not in robot_parsers:
        parser = RobotFileParser()
        parser.set_url(urljoin(domain, '/robots.txt'))
        parser.read()
        robot_parsers[domain] = parser
    return robot_parsers[domain].can_fetch(user_agent, url)
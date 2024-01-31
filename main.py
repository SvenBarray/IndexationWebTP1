from crawler.crawler import crawl

if __name__ == "__main__":
    start_url = "https://ensai.fr/"
    crawled_urls = crawl(start_url, courtesy_time= 20)
    print("\nCrawled URLs:")
    for url in crawled_urls:
        print(url)

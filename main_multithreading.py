from crawler.multithreading import multithreaded_crawl

if __name__ == "__main__":
    start_url = "https://ensai.fr/"
    crawled_urls = multithreaded_crawl(start_url, num_threads= 5, courtesy_time=3)
    print("\nCrawled URLs:")
    for url in crawled_urls:
        print(url)
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests as req
import csv
import time


class SiteCrawler:
    def __init__(self, start_url, depth):
        self.visited_links = []
        self.non_visited_links = []
        self.fetched_urls = []
        self.depth = depth

        self.__setup(start_url)

    def __update_depth(self):
        self.depth = self.depth - 1

    def __setup(self, start_url):
        res = req.get(start_url)
        html = res.text
        starting_page_doc = BeautifulSoup(html, "html.parser")

        links = starting_page_doc.find_all("a", href=True)

        # Fill list of links that need to be crawled
        for link in links:
            link_href = link['href']
            processed_link = urljoin(start_url, link_href)
            self.non_visited_links.append(processed_link)

    def fetch(self, url):
        while self.depth > 0:
            # Delay between each HTTP Request
            time.sleep(1)
            print("CURRENT SITE BEING CRAWLED: " + url + " | " + "CURRENT LEVEL: " + str(self.depth))

            res = req.get(url)
            # print(res.status_code)  # Find out HTML Status code
            # print(res.headers) # Important HTTP Headers
            # print(res.text) # HTML Code from response

            # HTML Code from response
            html = res.text
            doc = BeautifulSoup(html, "html.parser")

            link_list = []
            links = doc.find_all("a", href=True)

            # Make absolute paths out of relative paths from href attribute
            for link in links:
                link_href = link['href']
                processed_link = urljoin(url, link_href)
                link_list.append(processed_link)

            # Add the fetched URLs of the current site to the crawler's URL list
            self.fetched_urls.extend(link_list)

            visited_link = self.non_visited_links.pop(0)
            self.visited_links.append(visited_link)

            self.__update_depth()

            # Move on to the next Site recursively
            next_url = self.non_visited_links.__getitem__(0)
            self.fetch(next_url)

        for fetched_url in self.fetched_urls:
            print(fetched_url)

        print("FETCHED URLS: " + str(len(self.fetched_urls)))
        print("VISITED URLS: " + str(len(self.visited_links)))

        with open('links.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for url in self.fetched_urls:
                filewriter.writerow([url])


crawler = SiteCrawler("https://www.uni-muenchen.de/index.html", 5)
crawler.fetch(crawler.non_visited_links.__getitem__(0))

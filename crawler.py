from Crawler.SiteCrawler import SiteCrawler

crawler = SiteCrawler("https://www.uni-muenchen.de/index.html", 5)
crawler.fetch(crawler.non_visited_links.__getitem__(0))

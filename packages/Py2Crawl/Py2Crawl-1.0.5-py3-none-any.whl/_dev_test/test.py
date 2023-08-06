from Py2Crawl.py2crawl import Py2Crawl
from Py2Crawl.spider import Py2CrawlSpider
from Py2Crawl.http.methods import Py2CrawlMethods
from Py2Crawl.parser.parser import HTMLParser
from Py2Crawl.utils.request import Request
from Py2Crawl.output import json_output
from urllib.parse import urlparse
from PySide2.QtWidgets import QApplication
import asyncio
import time

res = {}


async def main(app):
    global res
    res = {}
    async def test_func(response):
        res.update({"url": response.url, "cookies": response.cookies})
        parser = HTMLParser(response.content)
        c = await parser.get_lxml_obj()
        print(response.url)
        """
        try:
            l = await parser.get_all_links_from_scope(str(response.url))
            to_scrape = []
            for i in l:
                if not i or not len(i) > 0:
                    continue
                if str(i).startswith("#"):
                    continue
                to_scrape.append(f"https://{urlparse(str(response.url)).netloc}{str(i)}")
            for i in to_scrape:
                r = Request(
                    url=str(i),
                    method=Py2CrawlMethods.PW_GET
                )
                await spider.execute(r)
        except:
            pass
        """

    crawler = Py2Crawl()
    spider = Py2CrawlSpider(
        start_urls=["https://secjur.com/"],
        start_urls_method=Py2CrawlMethods.PW_GET,
        callback=test_func,
        q_app=app
    )
    await crawler.crawl(spider)
    await json_output("test.json", res)


if __name__ == "__main__":
    s_time = time.time()
    app = QApplication([])
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(app))
    except RuntimeError as e:
        print("Loop closed!! ", e)
    finally:
        loop.close()
        sp_time = time.time()
    print("Time: ", sp_time - s_time)

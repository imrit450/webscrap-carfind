from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import sqlite3

from webscrap.spiders.carsales_mu import CarsalesMuSpider
from webscrap.spiders.motorsmega_mu import MyMotorMegaMuSpider
from webscrap.spiders.mycar_mu import MycarMuSpider

# Enable logging for CrawlerRunner
from webscrap.spiders.weshare_mu import WeShareMuItemSpider

configure_logging()

runner = CrawlerRunner(settings=get_project_settings())

conn = sqlite3.connect("mycars.db")
curr = conn.cursor()

#Delete Table data
curr.execute("""DELETE FROM cars_tbl""")

runner.crawl(MycarMuSpider)
runner.crawl(MyMotorMegaMuSpider)
runner.crawl(CarsalesMuSpider)
runner.crawl(WeShareMuItemSpider)


deferred = runner.join()
deferred.addBoth(lambda _: reactor.stop())

reactor.run()  # the script will block here until all crawling jobs are finished


import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import sqlite3

#
from webscrap.spiders.carsales_mu import CarsalesMuSpider
from webscrap.spiders.motorsmega_mu import MyMotorMegaMuSpider
from webscrap.spiders.mycar_mu import MycarMuSpider
from webscrap.spiders.weshare_mu import WeShareMuItemSpider

setting = get_project_settings()
process = CrawlerProcess(setting)

connection = sqlite3.connect("mycars.db")
cursor = connection.cursor()
cursor.execute("""DELETE FROM cars_tbl""")
connection.commit()
connection.close()

configure_logging()
settings = get_project_settings() # settings not required if running
runner = CrawlerRunner(settings)  # from script, defaults provided
runner.crawl(CarsalesMuSpider) # your loop would go here
runner.crawl(MyMotorMegaMuSpider)
runner.crawl(WeShareMuItemSpider)
runner.crawl(MycarMuSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until all crawling jobs are finished

# # Enable logging for CrawlerRunner
# from webscrap.spiders.weshare_mu import WeShareMuItemSpider

# configure_logging()
#
# runner = CrawlerRunner(settings=get_project_settings())
#
# conn = sqlite3.connect("mycars.db", timeout =15)
# curr = conn.cursor()
#
# #Delete Table data
# curr.execute("""DELETE FROM cars_tbl""")
#
# runner.crawl(MycarMuSpider)
# runner.crawl(MyMotorMegaMuSpider)
# runner.crawl(CarsalesMuSpider)
# runner.crawl(WeShareMuItemSpider)
#
#
# deferred = runner.join()
# deferred.addBoth(lambda _: reactor.stop())
#
# reactor.run()  # the script will block here until all crawling jobs are finished





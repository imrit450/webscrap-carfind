# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3


class CarsPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("mycars.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DELETE FROM cars_tbl WHERE lower(car_source) = 'mycar.mu'""")
        # mycar.mu
        # motors.mega.mu
        # weshare.mu
        # carsales_mu

        # self.curr.execute("""CREATE TABLE cars_tbl(
        #         car_title text,
        #         car_make text,
        #         car_model text,
        #         car_price integer,
        #         car_link text,
        #         car_mileage integer,
        #         car_year text,
        #         car_transmission text,
        #         car_status text,
        #         car_image_link text,
        #         car_source text,
        #         car_posted_date text,
        #         car_engine_capacity text
        #         )""")
        pass

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, items):
        self.curr.execute("""INSERT INTO cars_tbl values(?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            items['car_title'],
            items['car_make'],
            items['car_model'],
            items['car_price'],
            items['car_link'],
            items['car_mileage'],
            items['car_year'],
            items['car_transmission'],
            items['car_status'],
            items['car_image_link'],
            items['car_source'],
            items['car_posted_date'],
            items['car_engine_capacity']
        ))
        self.conn.commit()

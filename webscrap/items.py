# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def remove_nt(value):
    return value.replace("\t", '').replace("\n", '')


def remove_dash(value):
    return value.replace("-", '')


class MyCarMuItem(scrapy.Item):
    car_title = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                             output_processor=TakeFirst())
    car_make = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                            output_processor=TakeFirst())
    car_model = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt, remove_dash),
                             output_processor=TakeFirst())
    car_price = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                             output_processor=TakeFirst())
    car_link = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                            output_processor=TakeFirst())
    car_mileage = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                               output_processor=TakeFirst())
    car_year = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                            output_processor=TakeFirst())
    car_transmission = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                    output_processor=TakeFirst())
    car_status = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                              output_processor=TakeFirst())
    car_image_link = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                  output_processor=TakeFirst())
    car_source = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                              output_processor=TakeFirst())
    car_posted_date = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                   output_processor=TakeFirst())

    car_engine_capacity = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                       output_processor=TakeFirst())


class CarSalesMU(scrapy.Item):
    car_title = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                             output_processor=TakeFirst())
    car_make = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                            output_processor=TakeFirst())
    car_model = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt, remove_dash),
                             output_processor=TakeFirst())
    car_price = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                             output_processor=TakeFirst())
    car_link = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                            output_processor=TakeFirst())
    car_mileage = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                               output_processor=TakeFirst())
    car_year = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                            output_processor=TakeFirst())
    car_transmission = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                    output_processor=TakeFirst())
    car_status = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                              output_processor=TakeFirst())
    car_image_link = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                  output_processor=TakeFirst())
    car_source = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                              output_processor=TakeFirst())
    car_posted_date = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                   output_processor=TakeFirst())

    car_engine_capacity = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                       output_processor=TakeFirst())


class WeShareMuItem(scrapy.Item):
    car_title = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                             output_processor=TakeFirst())
    car_make = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                            output_processor=TakeFirst())
    car_model = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt, remove_dash),
                             output_processor=TakeFirst())
    car_price = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                             output_processor=TakeFirst())
    car_link = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                            output_processor=TakeFirst())
    car_mileage = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                               output_processor=TakeFirst())
    car_year = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                            output_processor=TakeFirst())
    car_transmission = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                    output_processor=TakeFirst())
    car_status = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                              output_processor=TakeFirst())
    car_image_link = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                  output_processor=TakeFirst())
    car_source = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                              output_processor=TakeFirst())
    car_posted_date = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                   output_processor=TakeFirst())

    car_engine_capacity = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                       output_processor=TakeFirst())


class MotorsMegaMu(scrapy.Item):
    car_title = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                             output_processor=TakeFirst())
    car_make = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                            output_processor=TakeFirst())
    car_model = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt, remove_dash),
                             output_processor=TakeFirst())
    car_price = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                             output_processor=TakeFirst())
    car_link = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                            output_processor=TakeFirst())
    car_mileage = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                               output_processor=TakeFirst())
    car_year = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                            output_processor=TakeFirst())
    car_transmission = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                    output_processor=TakeFirst())
    car_status = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                              output_processor=TakeFirst())
    car_image_link = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                  output_processor=TakeFirst())
    car_source = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                              output_processor=TakeFirst())
    car_posted_date = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                   output_processor=TakeFirst())

    car_engine_capacity = scrapy.Field(input_processor=MapCompose(str.strip, remove_nt),
                                       output_processor=TakeFirst())

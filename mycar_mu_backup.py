import scrapy
from scrapy import Request

from webscrap.items import MyCarMuItem
from webscrap.items import MauriceMotorsItem
from scrapy.loader import ItemLoader
from datetime import date
import re


def remove_nt(value):
    return value.replace("\t", '').replace("\n", '')


def remove_dash(value):
    return value.replace("-", '')


def convert_to_int(value):
    value = int(''.join(e for e in value if e.isnumeric()))
    return value


class MycarMuSpider(scrapy.Spider):
    name = 'mycar_mu_backup'
    page_number = 2
    start_urls = [
        'https://www.mycar.mu/car/buy?page=1'
    ]

    def parse(self, response):
        current_date = date.today()
        month = str(date(1900, current_date.month, 1).strftime('%B'))[0:3]
        year = str(current_date.year)
        new_car_date = month + ' ' + year
        car = MyCarMuItem()

        for cars in response.xpath("//*[@class='col-sm-6  col-md-4  d-flex']"):
            car_title = remove_nt(cars.css('.title span::text').extract_first())
            car_make = remove_nt(cars.css('.title span::text').extract_first()).split()[0]
            car_model = cars.css('.title span small::text').extract_first()

            car_price = convert_to_int(cars.css('.price::text').extract_first())
            car_link = cars.css('.title::attr(href)').extract_first()
            car_mileage = cars.css('.description+ .condition-list li+ li span::text').extract_first()
            car_year = cars.css('.condition-list+ .condition-list li+ li span::text').extract_first()
            car_transmission = cars.css('.condition-list+ .condition-list li:nth-child(1) span::text').extract_first()
            car_status = cars.css('.description+ .condition-list li:nth-child(1) span::text').extract_first()
            car_image_link = cars.css('.display-listing-images .image-holder img::attr(src)').extract_first()

            car_details_page = response.urljoin(car_link)

            # Check if Car has a model
            if car_model is None:
                car_model = ''
            else:
                car_model = remove_dash(car_model)

            # Check if Car is new
            if car_mileage is None:
                car_mileage = ''
                car_year = new_car_date
            else:
                car_mileage = convert_to_int(car_mileage)

            car['car_title'] = car_title
            car['car_make'] = car_make
            car['car_model'] = car_model
            car['car_price'] = car_price
            car['car_link'] = car_link
            car['car_mileage'] = car_mileage
            car['car_year'] = car_year
            car['car_transmission'] = car_transmission
            car['car_status'] = car_status
            car['car_image_link'] = car_image_link
            car['car_source'] = 'MyCar.mu'

            yield Request(car_details_page, meta={'cars': car}, callback=self.parse_details, dont_filter=True)

            # car['car_posted_date'] = car_posted_date
        next_page = 'https://www.mycar.mu/car/buy?page=' + str(MycarMuSpider.page_number)

        if MycarMuSpider.page_number <= 2:
            MycarMuSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_details(self, response):
        car = response.meta['cars']
        print(car['car_title'])
        car_posted_date = response.css('li:nth-child(11) span::text').extract_first()
        if car_posted_date is None:
            car_posted_date = ''
        else:
            car_posted_date = car_posted_date
        car['car_posted_date'] = car_posted_date
        yield 




class MauriceMotorsSpider(scrapy.Spider):
    name = 'mauricemotors_backup'
    page_number = 2
    allowed_domains = ['mauricemotors.mu']
    start_urls = [
        'https://www.mauricemotors.mu/?order_by=date_created&filters=no&order_to=desc&page=1'
    ]

    def parse(self, response):
        print(response.selector.xpath("//*[@class='itemsContainer']"))
        for cars in response.selector.xpath("//*[@class='itemsContainer']"):
            loader = ItemLoader(item=MauriceMotorsItem(), selector=cars, response=response)
            car_make = response.css('strong span::text').extract()[0]
            car_year = response.css('.link strong::text').extract()[0]
            car_title = car_year + car_make
            loader.add_css('car_title', car_title)
            loader.add_value('car_make', car_make)
            loader.add_css('car_model', '.link span::text')
            loader.add_css('car_price', '.price::text')
            loader.add_css('car_link', '.link::attr(href)')
            loader.add_css('car_mileage', '.mileage::text')
            loader.add_value('car_year', car_year)
            loader.add_css('car_transmission', '.transmission::text')
            loader.add_value('car_status', 'Not found')
            car_image = response.css('#content_box .lazyloaded::attr(style)').extract()[0]
            car_image_link = car_image.lstrip('url("').rstrip('")')
            loader.add_value('car_image_link', car_image_link)

            yield loader.load_item()

        next_page = 'https://www.mauricemotors.mu/?order_by=date_created&filters=no&order_to=desc&page=' + str(
            MauriceMotorsSpider.page_number)

        if MauriceMotorsSpider.page_number <= 2:
            MauriceMotorsSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

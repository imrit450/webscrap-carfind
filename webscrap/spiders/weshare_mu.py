from urllib.parse import urljoin

import scrapy

from ..items import WeShareMuItem
from datetime import datetime, date, timedelta


def remove_nt(value):
    return value.replace("\t", '').replace("\n", '').strip()


def remove_dash(value):
    return value.replace("-", '')


def convert_to_int(value):
    if value is None or value.isalpha():
        value = -1
    else:
        value = int(float(''.join(e for e in value if e.isnumeric())))
    return value


def get_rundate():
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    return dt_string


def get_yesterday_date():
    # datetime object containing current date and time
    # dd/mm/YY H:M:S
    dt_string = datetime.strftime(datetime.now() - timedelta(1), "%d/%m/%Y %H:%M:%S")

    return dt_string


def get_date():
    current_date = date.today()
    month = str(date(1900, current_date.month, 1).strftime('%B'))[0:3]
    year = str(current_date.year)
    date_year = month + ' ' + year
    return date_year


class WeShareMuItemSpider(scrapy.Spider):
    name = 'weshare_mu'
    page_number = 2
    allowed_domains = ['weshare.mu']

    start_urls = [
        'https://weshare.mu/offres?category=7&ncid=12&page=1'
    ]

    def parse(self, response):
        car = WeShareMuItem()
        base_url = "https://weshare.mu/"

        for car_selector in response.xpath("//*[@class='col-12 col-sm-6 col-md-4 col-lg-3 p-1 p-sm-2']"):
            car_link = urljoin(base_url, car_selector.css('a::attr(href)').extract_first())
            car_image_link = urljoin(base_url, car_selector.css(' .photo img::attr(data-src)').extract_first())
            yield response.follow(
                car_link,
                callback=self.parse_car_details,
                cb_kwargs={'car': car, 'car_link': car_link, 'base_url': base_url, 'car_image_link': car_image_link},
                dont_filter=True
            )
        print("Page number: " + str(WeShareMuItemSpider.page_number))

        next_page = "https://weshare.mu/offres?category=7&ncid=12&page=" + str(WeShareMuItemSpider.page_number)
        if WeShareMuItemSpider.page_number <= 10:
            WeShareMuItemSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_car_details(self, response, car, car_link, base_url, car_image_link):

        title = remove_nt(str(response.css('.big::text').extract_first()))
        title = title.split(" - ", 3)
        car_make = title[0]
        car_model = title[1]
        car_year = title[2]
        car_title = str(' '.join(title))
        print(car_title)

        key = []
        value = []

        for specs in response.css(".list-group-item table tr"):
            key.append(specs.xpath("./td[position()=1]/text()").extract())
            value.append(specs.xpath("./td[position()=2]/text()").extract())
        # Flatten the lists and extract the text :
        keys = [item.replace(" :", "") for sublist in key for item in sublist]

        values = [item for sublist in value for item in sublist]

        # Create the dictionary :
        spec_dict = dict(zip(keys, values))
        print(spec_dict)

        if 'Kilométrage' not in spec_dict:
            car_mileage = -1
        else:
            car_mileage = spec_dict['Kilométrage']
            car_mileage = convert_to_int(car_mileage)

        car_transmission = spec_dict['Boite de vitesses']
        car_status = 'None'
        car_engine_capacity = spec_dict['Cylindrée']
        # car_image_link = urljoin(base_url, response.css('.slides img::attr(src)').extract_first())

        car_price = response.css('.view .card-price::text').extract_first()
        car_price = convert_to_int(car_price)
        car_image_link = car_image_link
        car_posted_date = remove_nt(response.xpath('.//*[@class="card-date"]/text()').extract()[1])

        if "Aujourd'hui" in car_posted_date:
            car_posted_date = get_rundate()
        elif "Hier" in car_posted_date:
            car_posted_date = get_yesterday_date()

        car['car_title'] = car_title
        car['car_price'] = car_price
        car['car_make'] = car_make
        car['car_model'] = car_model
        car['car_mileage'] = car_mileage
        car['car_year'] = car_year
        car['car_transmission'] = car_transmission
        car['car_status'] = car_status
        car['car_image_link'] = car_image_link
        car['car_source'] = 'weshare.mu'
        car['car_posted_date'] = car_posted_date
        car['car_engine_capacity'] = car_engine_capacity
        car['car_link'] = car_link

        yield car

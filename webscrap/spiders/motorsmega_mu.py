from urllib.parse import urljoin

import scrapy

from ..items import MotorsMegaMu
from datetime import datetime, date


def remove_nt(value):
    return value.replace("\t", '').replace("\n", '')


def remove_dash(value):
    return value.replace("-", '')

def containsNumber(value):
    return any([char.isdigit() for char in value])

def convert_to_int(value):
    if value is None or value.isalpha():
        value = -1
    elif containsNumber(value):
        value = int(float(''.join(e for e in value if e.isnumeric())))
    else:
        value = -1
    return value



def get_rundate():
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    return dt_string


def get_date():
    current_date = date.today()
    month = str(date(1900, current_date.month, 1).strftime('%B'))[0:3]
    year = str(current_date.year)
    date_year = month + ' ' + year
    return date_year


class MyMotorMegaMuSpider(scrapy.Spider):
    name = 'motorsmega_mu'
    page_number = 2
    allowed_domains = ['motors.mega.mu']
    start_urls = [
        'https://motors.mega.mu/auto/search/1/?withPhoto=on&onlyActual=on'
    ]

    def parse(self, response):
        car = MotorsMegaMu()

        for index, car_selector in enumerate(response.xpath("//*[@class='mdl-list__item ad-row']")):
            car_link = 'https://motors.mega.mu' + str(car_selector.css('.ad-photo::attr(href)').extract_first())
            # car_image_link = car_selector.css('.ad-icon .cover::attr(src)').extract_first()

            yield response.follow(
                car_link,
                callback=self.parse_car_details,
                cb_kwargs={'car': car, 'car_link': car_link},
                dont_filter=True
            )
        print("Page number: " + str(MyMotorMegaMuSpider.page_number))
        next_page_url = str(MyMotorMegaMuSpider.page_number) + "/?withPhoto=on&onlyActual=on"
        next_page = urljoin("https://motors.mega.mu/auto/search/", next_page_url)
        print(next_page)
        if MyMotorMegaMuSpider.page_number <= 25:
            MyMotorMegaMuSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_car_details(self, response, car, car_link):

        car_title = remove_nt(response.css('h1::text').extract_first())
        car_title = car_title.split("'", 1)[1]
        car_make = car_title.split(" ", 2)[1]

        car_model = car_title.split(" ", 2)
        if len(car_model) == 3:
            car_model = car_model[2]
        else:
            car_model = 'None'
        specs = response.css('.misc-table span+ span::text').extract()
        status = ['Good', 'Excellent', 'Normal']
        transmission = ['Manual', 'Automatic']

        car_mileage = response.css('.misc-table div:nth-child(4) span+ span::text').extract_first()
        car_transmission = response.css('.misc-table div:nth-child(8) span+ span::text').extract_first()
        car_status = response.css('.misc-table div:nth-child(2) span+ span::text').extract_first()
        car_engine_capacity = response.css('.misc-table div:nth-child(6) span+ span::text').extract_first()
        car_image_link = response.css('.photos img::attr(src)').extract_first()

        for spec in specs:
            if 'cc' in spec:
                car_engine_capacity = spec
            elif 'km' in spec:
                car_mileage = spec
            elif any(word in spec for word in transmission):
                car_transmission = spec.split(",", 2)[0]
            elif any(word in spec for word in status):
                car_status = spec
        sold = response.css('.status::text').extract_first()
        if sold:
            car_status = 'Sold'

        car_price = response.css('.hdr .price::text').extract_first()

        if car_price is "Negotiable":
            car_price = 0
        else:
            car_price = convert_to_int(car_price)
        car_year = str(response.css('h1::text').extract_first()).split("'", 1)[0]

        car_image_link = car_image_link
        car_posted_date = response.css('.mdl-list__item:nth-child(4)::text').extract_first()

        car_mileage = convert_to_int(car_mileage)

        car['car_title'] = car_title
        car['car_price'] = car_price
        car['car_make'] = car_make
        car['car_model'] = car_model
        car['car_mileage'] = car_mileage
        car['car_year'] = car_year
        car['car_transmission'] = car_transmission
        car['car_status'] = car_status
        car['car_image_link'] = car_image_link
        car['car_source'] = 'motors.mega.mu'
        car['car_posted_date'] = car_posted_date
        car['car_engine_capacity'] = car_engine_capacity
        car['car_link'] = car_link

        yield car

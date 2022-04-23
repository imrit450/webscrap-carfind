import scrapy

from ..items import MyCarMuItem
from datetime import datetime, date


def remove_nt(value):
    return value.replace("\t", '').replace("\n", '')


def remove_dash(value):
    return value.replace("-", '')


def convert_to_int(value):
    if value.isalpha() or value is None:
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


def get_date():
    current_date = date.today()
    month = str(date(1900, current_date.month, 1).strftime('%B'))[0:3]
    year = str(current_date.year)
    date_year = month + ' ' + year
    return date_year


class MycarMuSpider(scrapy.Spider):
    name = 'mycar_mu'
    page_number = 2
    allowed_domains = ['mycar.mu']
    start_urls = [
        'https://www.mycar.mu/car/buy?page=1'
    ]

    def parse(self, response):
        car = MyCarMuItem()

        for index, car_selector in enumerate(response.xpath("//*[@class='col-sm-6  col-md-4  d-flex']")):
            car_link = car_selector.css('.title::attr(href)').extract_first()
            car_image_link = car_selector.css('.display-listing-images .image-holder img::attr(src)').extract_first()

            yield response.follow(
                car_link,
                callback=self.parse_car_details,
                cb_kwargs={'car': car, 'car_link': car_link, 'car_image_link': car_image_link},
                dont_filter=True
            )

        next_page = 'https://www.mycar.mu/car/buy?page=' + str(MycarMuSpider.page_number)

        if MycarMuSpider.page_number <= 25:
            MycarMuSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_car_details(self, response, car, car_link, car_image_link):
        new_car_date = get_rundate()
        new_car_year = get_date()
        car_title = remove_nt(response.css('.main-title::text').extract_first())
        car_make = car_title.split(" ", 1)[0]
        car_model = remove_dash(car_title.split(" ", 1)[1])
        car_status = response.css('.col-count li:nth-child(1) span::text').extract_first()
        print(car_status)
        car_price = convert_to_int(response.css('#price-dutypaid .price').extract_first())

        is_new = response.css('.topright::text').extract_first()
        if is_new:
            car_mileage = '0'
            car_year = new_car_year
            car_transmission = response.css('.col-count li:nth-child(3) span::text').extract_first()
            car_image_link = car_image_link
            car_posted_date = new_car_date
            car_engine_capacity = response.css('.col-count li:nth-child(5) span::text').extract_first()
        else:
            car_mileage = response.css('.col-count li:nth-child(3) span::text').extract_first()
            car_year = response.css('.col-count li:nth-child(2) span::text').extract_first().split(" ", 1)[1]
            car_transmission = response.css('.col-count li:nth-child(5) span::text').extract_first()

            car_image_link = car_image_link
            car_posted_date = response.css('.col-count li:nth-child(11) span::text').extract()
            if car_posted_date:
                car_posted_date = (response.css('.col-count li:nth-child(11) span::text').extract()[1])
            else:
                car_posted_date = (response.css('.col-count li:nth-child(10) span::text').extract()[1])
            car_engine_capacity = response.css('.col-count li:nth-child(7) span::text').extract_first()

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
        car['car_source'] = 'mycar.mu'
        car['car_posted_date'] = car_posted_date
        car['car_engine_capacity'] = car_engine_capacity
        car['car_link'] = car_link

        yield car

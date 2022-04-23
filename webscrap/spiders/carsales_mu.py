import scrapy
from datetime import date
from ..items import CarSalesMU


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
    current_date = date.today()
    month = str(date(1900, current_date.month, 1).strftime('%B'))[0:3]
    year = str(current_date.year)
    new_car_date = month + ' ' + year
    return new_car_date


class CarsalesMuSpider(scrapy.Spider):
    name = 'carsales_mu'
    page_number = 2
    allowed_domains = ['carsales.mu']
    start_urls = [
        'https://www.carsales.mu/'
    ]

    def parse(self, response):
        car = CarSalesMU()

        for index, car_selector in enumerate(response.xpath("//*[@class='col-md-4 col-lg-6 col-xl-4']")):
            car_link = car_selector.css('.product-classic-title a::attr(href)').extract_first()

            car_image_link = car_selector.css('.product-classic-media a img::attr(data-src)').extract_first()

            yield response.follow(
                car_link,
                callback=self.parse_car_details,
                cb_kwargs={'car': car, 'car_link': car_link, 'car_image_link': car_image_link},
                dont_filter=True
            )

    def parse_car_details(self, response, car, car_link, car_image_link):
        title_split = remove_nt(response.css('.heading-2::text').extract_first())
        title_split = title_split.split(" ", 2)

        car_title = response.css('.heading-2::text').extract_first().split(" ", 1)[1]
        car_make = str(title_split[1])
        car_model = str(title_split[2])
        car_status = response.css('.misc-table div:nth-child(2)::text').extract_first()
        if not car_status:
            car_status = response.css('.col-xl-8 div:nth-child(4)::text').extract_first()
        car_status = car_status.split(":", 1)[1]

        car_price = convert_to_int(response.css('.price::text').extract_first())

        car_mileage = response.css('.misc-table div:nth-child(3)::text').extract_first()
        if not car_mileage:
            car_mileage = response.css('div:nth-child(5)::text').extract_first()
        car_mileage = car_mileage.split(":", 1)[1]

        car_year = title_split[0]
        car_transmission = response.css('.misc-table div:nth-child(6)::text').extract_first()
        if not car_transmission:
            car_transmission = response.css('div:nth-child(8)::text').extract_first()
        car_transmission = car_transmission.split(":", 1)[1]

        car_image_link = car_image_link
        car_posted_date = response.css('.blog-post-solo-footer-list a::text').extract_first()
        specs = response.css('dd::text').extract()
        transmission = ['Manual', 'Automatic']
        for spec in specs:
            if 'cc' in spec:
                car_engine_capacity = spec
            elif 'Kms' in spec:
                car_mileage = spec
            elif any(word in spec for word in transmission):
                car_transmission = spec

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
        car['car_source'] = 'carsales.mu'
        car['car_posted_date'] = car_posted_date
        car['car_engine_capacity'] = car_engine_capacity
        car['car_link'] = car_link

        yield car

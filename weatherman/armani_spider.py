import scrapy


class ArmaniSpider(scrapy.Spider):
    name = "armani_spider"
    allowed_domains = ["armani.com"]
    start_urls = ["https://www.armani.com/en-us/experience/armani-exchange"]

    def parse(self, response):
        category_links = response.css('#mainMenu > div:nth-child(2) > div > ul > li > a::attr(href)').getall()
        category_links = [response.urljoin(link) for link in category_links if 'armani-exchange' in link]

        for category in category_links:
            yield response.follow(category, self.parse_category)

    def parse_category(self, response):
        product_urls = response.css('item-card.item-card > a::attr(href)').getall()
        for url in product_urls:
            yield response.follow(url, self.parse_product)

        next_page = response.css('link[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_category)

    def parse_product(self, response):

        product_data = {
            "retailer_sku": None,
            "trail": [],
            "gender": "",
            "category": [],
            "brand": None,
            "url": response.url,
            "market": "US",
            "retailer": "armani-us",
            "name": None,
            "description": [],
            "care": [],
            "image_urls": None,
            "skus": None,
            "price": None,
            "currency": None
        }

        category = response.css('.header-topbar > .header-hub > a.header-hub__title::text').get()
        product_data["category"].append(category)

        product_info_box = response.css('div.item-content__right .item-shop-panel')
        if product_info_box:

            brand = product_info_box.css('.item-shop-panel__topbar > .item-shop-panel__brand::text').get()
            product_data["brand"] = brand

            name = product_info_box.css('.item-shop-panel > h1::text').get().strip()
            product_data["name"] = name

            description = product_info_box.css('.item-shop-panel__description > p > span::text').get()
            if description:
                product_data["description"].append(description.strip())

            product_code_lst = product_info_box.css('.item-shop-panel__modelfabricolor > p.attributes')
            if product_code_lst:
                text = product_code_lst.css('span.text::text').get()
                product_data["description"].append(text)
                value = product_code_lst.css('span.value::text').get()
                product_data["description"].append(value)

            technical_description = product_info_box.css('.item-shop-panel__details > p.attributes')
            if technical_description:
                technical_description_lst = technical_description.css('span.value::text').getall()
                for tech_describe in technical_description_lst:
                    product_data["description"].append(tech_describe.strip())

            product_care = product_info_box.css('.item-shop-panel__details')
            if product_care and "Details" in product_care.css('h4.item-shop-panel__tile::text').get():
                care = product_info_box.css('.item-shop-panel__details > p::text').get()
                product_data["care"].append(care)

            price_info = product_info_box.css('.item-shop-panel__price span[class="price"]')
            if price_info:
                currency = price_info.css('span.currency::text').get()
                if currency == "$":
                    product_data["currency"] = 'USD'
                price = price_info.css('span.value::text').get()
                product_data["price"] = price

            image_urls = {}
            image_blocks = response.css('div.product-variations div.swatch-item')
            for block in image_blocks:
                color = block.css('::attr(data-color-name)').get()
                images = block.css('img::attr(data-src)').getall()
                image_urls[color] = [response.urljoin(img) for img in images]

        yield product_data

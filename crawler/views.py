import requests
from bs4 import BeautifulSoup
import bs4
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import models


class Crawler:
    def __init__(self, url, method="GET"):
        self.url = url
        self.method = method
        self._response = None

    @property
    def content(self):
        print(self._response.content)
        return self._response.content if self._response else None

    def send_request(self):
        self._response = requests.request(self.method, self.url)

    def make_it_bs4(self):
        return BeautifulSoup(self.content, features="lxml") if self.content else None

    def build_url(
            self,
    ):
        raise NotImplementedError


class NewEggCrawler(Crawler):
    def __init__(self, product_id):
        self.product_id = product_id

        super().__init__(self.build_url())

    def build_url(self):
        return "https://www.newegg.com/p/{id}".format(id=self.product_id)


class Element:
    """
    every elements classes will extend this and if there weren't any parse it will raise an exception
    """

    def __init__(self, dom):
        self.dom = dom

    def parse(self):
        raise NotImplementedError


class TitleElement(Element):
    def parse(self):
        return (
            self.dom.body.find("div", id="app").find("h1", class_="product-title").text
        )


class BrandElement(Element):
    def parse(self):
        brand = (
            (
                self.dom.body.find("div", id="app")
                    .find("div", class_="page-section-inner")
                    .find("div", class_="product-section")
                    .find("div", class_="product-additional-info display-flex")
            )
                .find_all(class_="info-cell")[-1]
                .text.split()[-1]
        )
        # print("*" * 40)
        # print(brand)
        return brand


class MainPriceElement(Element):
    def parse(self):
        main = self.dom.body.find("li", class_="price-was").text[1:]
        main = main.replace(",", "")
        main = float(main) if main else None
        return main


class DealPriceElement(Element):
    def parse(self):
        deal = (
                self.dom.body.find("li", class_="price-current").find("strong").text
                + self.dom.body.find("li", class_="price-current").find("sup").text
        )
        deal = deal.replace(",", "")
        deal = float(deal) if deal else None
        return deal


class SellerElement(Element):
    def parse(self):
        return (
            self.dom.body.find("div", id="app")
                .find("div", class_="page-content")
                .find("div", class_="row-side")
                .find("strong")
                .text
        )


class StarsElement(Element):
    def parse(self):
        try:
            stars = (
                self.dom.body.find("div", id="app")
                    .find("div", class_="page-content")
                    .find("div", class_="row-body")
                    .find("div", class_="product-rating")
                    .find("i")["class"][-1][-1]
            )
            stars = int(stars)
        except TypeError:
            stars = None
        return stars


class CountElement(Element):
    def parse(self):
        count = (
            self.dom.body.find("div", id="app")
                .find("div", class_="page-content")
                .find("div", class_="row-body")
                .find("div", class_="product-reviews")
                .find("span")
                .text[1:-1]
        )
        count = count.replace(",", "")
        try:
            count = float(count)
        except ValueError:
            count = None
        return count


class MainImageElement(Element):
    def parse(self):
        return (
            self.dom.body.find("div", id="app")
                .find("div", class_="row-body")
                .find("div", class_="swiper-zoom-container")
                .img["src"]
        )


class ImagesElement(Element):
    def parse(self):
        images = []
        tags = (
            self.dom.body.find("div", id="app")
                .find("div", class_="row-body")
                .find("div", class_="product-view")
                .find("div", class_="swiper-gallery-thumbs")
                .find("div", class_="swiper-wrapper")
                .find_all()
        )
        for tag in tags:
            try:
                images.append(tag["src"])
            except KeyError:
                continue

        return images


class FeaturesElement(Element):
    def parse(self):
        features_ = (
            self.dom.body.find("div", id="app")
                .find("div", class_="row-body")
                .find("div", class_="product-wrap")
                .find("div", class_="product-bullets")
                .find("ul")
                .find_all("li")
        )
        features = [li.text.strip() for li in features_]
        return features


class Parser:
    def __init__(self, dom):
        self.dom = dom

    def get_elements(self):
        return [
            (attribute, getattr(self, attribute)) for attribute in self.Meta.attributes
        ]

    def get_result(self):
        result = {}
        for attribute, element in self.get_elements():
            result[attribute] = element(self.dom).parse()
        return result


class NewEggParser(Parser):
    title = TitleElement
    brand = BrandElement
    main_price = MainPriceElement
    deal_price = DealPriceElement
    seller = SellerElement
    stars = StarsElement
    count = CountElement
    main_image = MainImageElement
    images = ImagesElement
    features = FeaturesElement

    class Meta:
        attributes = (
            "title",
            "brand",
            "main_price",
            "deal_price",
            "seller",
            "stars",
            "count",
            "main_image",
            "images",
            "features",
        )


def newegg(request, product_id):
    crawler = NewEggCrawler(product_id)
    crawler.send_request()
    html = crawler.make_it_bs4()
    parser = NewEggParser(html)
    result = parser.get_result()

    product = models.Product(
        title=result["title"],
        brand=result["brand"],
        main_price=result["main_price"],
        deal_price=result["deal_price"],
        seller=result["seller"],
        stars=result["stars"],
        count=result["count"],
        main_image=result["main_image"],
    )

    product.save()
    for feature in result["features"]:
        models.Feature.objects.create(content=feature, product=product)

    for image in result["images"]:
        models.Images.objects.create(content=image, product=product)

    return JsonResponse(result)


def show(request):
    product = models.Product.objects.all().last()
    features = models.Feature.objects.filter(product=product)
    return render(request, "product.html", {"product": product, "features": features})



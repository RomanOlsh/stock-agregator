import pymongo
from bson import ObjectId
from django.utils.timezone import now

from stocks.models import Company, Stock
from django.core.management.base import BaseCommand, CommandError
from lxml import html
import os


class Command(BaseCommand):

    XPATH_PRICE = '//*[@id="quote-market-notice"]/ancestor::div/span[1]/text()'

    XPATH_NAME = '//*[@data-test="quote-header"]/descendant::h1/text()'

    def handle(self, *args, **options):
        mongo_client = pymongo.MongoClient(os.environ.get('MONGO_URL'))
        db = mongo_client[os.environ.get('MONGO_DB')]
        page_collection = db[os.environ.get('MONGO_COLLECTION')]

        self.parse_pages(page_collection)

        # get a bulk of unarchived (10)
        # mark them as archived (find better way to lock them)
        # parse name and price and save to stock db (createdAt is taken from page)

    def parse_pages(self, page_collection):
        for page_object in page_collection.find({"archivedAt": ""}):
            parsed_page = html.fromstring(page_object["page"])
            price = parsed_page.xpath(self.XPATH_PRICE)[0]
            name = parsed_page.xpath(self.XPATH_NAME)[0]
            self.stdout.write("price: {}, name: {}".format(price, name))

            # Create new stock:
            company = Company.objects.get(name=name)
            stock = Stock(price=price, company=company, pub_date=page_object["createdAt"])
            stock.save()

            # Archive page:
            page_collection.find_one_and_update(
                {"_id": ObjectId(page_object["_id"])},
                {"$set": {"archivedAt": now()}}, upsert=True
            )

            # Update company:
            self.update_company(company)

    def update_company(self, company):
        stocks = Stock.objects.filter(company__name=company.name, pub_date__gt=company.updated_at).order_by('pub_date')
        if stocks:
            new_stock = stocks[0]

            if new_stock.price > company.current_price:
                status = "UP"
            elif new_stock.price < company.current_price:
                status = "DOWN"
            else:
                status = company.stock_status

            self.stdout.write("updating company's price: {}, date: {} and status: {}"
                              .format(new_stock.price, new_stock.pub_date, status))
            company.updated_at = new_stock.pub_date
            company.current_price = new_stock.price
            company.stock_status = status
            company.save()
        else:
            self.stdout.write("Stocks DB is empty")

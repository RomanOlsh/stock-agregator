from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from stocks.models import Company
import requests
import pymongo
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        mongo_client = pymongo.MongoClient(os.environ.get('MONGO_URL'))
        db = mongo_client[os.environ.get('MONGO_DB')]
        page_collection = db[os.environ.get('MONGO_COLLECTION')]

        for company in Company.objects.all():
            self.collect_and_save(company.url, page_collection)

    def collect_and_save(self, url, page_collection):
        xml_page = requests.get(url)
        page_object = {"createdAt": now(), "page": xml_page.content, "archivedAt": ""}
        insert_result = page_collection.insert_one(page_object)
        self.stdout.write(str(insert_result.inserted_id))

from django.db import models
from django.utils.timezone import now


class Company(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    current_price = models.DecimalField(max_digits=5, decimal_places=2)
    stock_status = models.CharField(max_length=50, default="NONE")
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return "{}, Current Price: {}, Status: {}, Updated at: {}"\
            .format(self.name, self.current_price, self.stock_status, self.updated_at)


class Stock(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pub_date = models.DateTimeField(default=now, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Company: {}, Price: {}, Date: {}".format(self.company.name, self.price, self.pub_date)

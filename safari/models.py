from django.db import models
from django.db.models import Q
from django.contrib.postgres.search import SearchRank


class Safari(models.Model):
    imageCover = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_price = models.DecimalField(max_digits=6, decimal_places=2)
    ratingsQuantity = models.IntegerField()
    ratingsAverage = models.DecimalField(max_digits=6, decimal_places=1)
    tour_data = models.JSONField()
    inclusions_data = models.JSONField()
    getting_there_data = models.JSONField()
    day_by_day = models.JSONField()

    class Meta:
        ordering = ["name"]
        verbose_name = "Safari Tour"

    def __str__(self):
        return self.name
    
    @staticmethod
    def search_by_price_and_max_price(price_range, max_price_range):
        return Safari.objects.filter(Q(price__range=price_range) | Q(max_price__range=max_price_range))
    
    @staticmethod
    def search_by_json_fields(vector, query):
        return Safari.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.1)
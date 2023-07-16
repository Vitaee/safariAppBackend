from django.db import models
from django.db.models import Q
from django.contrib.postgres.search import SearchRank
from rest_framework.exceptions import ValidationError
from django.conf import settings


class SafariRatings(models.Model):
    """
    This model holds safari tour's ratings
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    point = models.FloatField(verbose_name="Rating Point", blank=True)
    comment = models.CharField(max_length=200, verbose_name="Rating Comment", blank=True)



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
    ratings = models.ManyToManyField(SafariRatings, blank=True, verbose_name="User Ratings")

    class Meta:
        ordering = ["id"]
        verbose_name = "Safari Tour"

    def __str__(self):
        return self.name
    
    @staticmethod
    def search_by_price_and_max_price(price_range, max_price_range):
        return Safari.objects.filter(Q(price__range=price_range) | Q(max_price__range=max_price_range))
    
    @staticmethod
    def search_by_json_fields(vector, query):
        return Safari.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.1)

    @staticmethod
    def validate_price_range(price_min, price_max):
        if price_min is not None and price_min < 300:
            raise ValidationError("price_min should be at least 300")
        if price_max is not None and price_max < 400:
            raise ValidationError("price_max should be at least 400")
        if price_min is not None and price_max is not None and price_min > price_max:
            raise ValidationError("price_min should be less than or equal to price_max")
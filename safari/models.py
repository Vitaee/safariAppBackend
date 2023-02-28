from django.db import models

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

    def __str__(self):
        return self.name
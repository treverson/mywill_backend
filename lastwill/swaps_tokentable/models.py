from django.db import models


class Tokens(models.Model):
    address = models.CharField(max_length=50)
    token_name = models.CharField(max_length=512)
    token_short_name = models.CharField(max_length=64)
    decimals = models.IntegerField()
    image_link = models.CharField(max_length=512)

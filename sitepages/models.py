from django.db import models

# Create your models here.

class StaticPage(models.Model):
    page_name = models.CharField(max_length=30)
    order_num = models.
    meta_description = models.CharField(max_length=200)
    meta_keywords = models.CharField(max_length=160)
    date_created = models.DateField()
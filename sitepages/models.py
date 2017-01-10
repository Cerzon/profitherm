from django.db import models

# Create your models here.

class StaticPage(models.Model):
    page_name = models.CharField(max_length=80)
    meta_description = models.CharField(max_length=255)
    meta_keywords = models.CharField(max_length=255)
    date_created = models.DateTimeField()
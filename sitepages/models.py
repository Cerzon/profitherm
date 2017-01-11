from django.db import models

# Create your models here.

class StaticPage(models.Model):
    order_num = models.IntegerField()
    page_name = models.CharField(max_length=30)
    menu_text = models.CharField(max_length=30)
    is_published = models.BooleanField(default=False)
    meta_description = models.CharField(max_length=200)
    meta_keywords = models.CharField(max_length=160)
    date_created = models.DateField(auto_now_add=True)
    page_data = models.TextField()

    class Meta():
        ordering = ['order_num']
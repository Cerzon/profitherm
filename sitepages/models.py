from django.db import models

# Create your models here.

class StaticPage(models.Model):
    order_num = models.IntegerField()
    page_name = models.CharField(max_length=30)
    is_published = models.BooleanField(default=False)
    meta_description = models.CharField(max_length=200)
    meta_keywords = models.CharField(max_length=160)
    date_created = models.DateField(auto_now_add=True)
    page_content = models.TextField()
    page_head = models.TextField()
    page_scripts = models.TextField()

    class Meta():
        ordering = ['order_num']

    def __str__(self):
        return self.page_name


class UserFeedback(models.Model):
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=80)
    user_email = models.EmailField()
    message_header = models.CharField(max_length=160)
    message_text = models.TextField()

    class Meta():
        ordering = ['-date_created']

    def __str__(self):
        return self.message_header
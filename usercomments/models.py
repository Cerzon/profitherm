from django.db import models

# Create your models here.

class UserComment(models.Model):
    user_name = models.CharField(max_length=80, default="Аноним")
    user_email = models.EmailField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    comment_text = models.TextField()

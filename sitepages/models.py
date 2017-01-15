from django.db import models

# Create your models here.

class StaticPage(models.Model):
    is_published = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    order_num = models.SmallIntegerField()
    page_name = models.CharField(max_length=30)
    page_title = models.CharField(max_length=120)
    meta_description = models.CharField(max_length=200)
    meta_keywords = models.CharField(max_length=160)
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


class CalculationOrder(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=80)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=16)
    heated_area = models.SmallIntegerField()
    attachments = models.FileField(upload_to='/uploads/calc_order')
    radiator_heating = models.BooleanField(default=True)
    floor_heating = models.BooleanField(default=True)
    water_supply = models.BooleanField(default=True)
    water_treatment = models.BooleanField(default=False)
    sewerage = models.BooleanField(default=True)
    boilerplant = models.BooleanField(default=True)
    svc_project = models.BooleanField(default=True)
    svc_purchase = models.BooleanField(default=True)
    svc_assembly = models.BooleanField(default=True)
    svc_reconstruction = models.BooleanField(default=True)
    svc_maintenance = models.BooleanField(default=True)
    svc_consulting = models.BooleanField(default=True)

    class Meta():
        ordering = ['-date_created']

    def __str__(self):
        return 'Order #%s from %s' % (self.pk, self.date_created)


class ImageGallery(models.Model):
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    order_num = models.SmallIntegerField()
    gallery_name = models.CharField(max_length=40)
    gallery_description = models.TextField()
    gallery_styles = models.TextField()
    gallery_scripts = models.TextField()

    class Meta():
        ordering = ['order_num']

    def __str__(self):
        return self.gallery_name

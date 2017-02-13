from django.db import models

# Create your models here.

class StaticPage(models.Model):
    is_published = models.BooleanField(default=False)
    order_num = models.SmallIntegerField()
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=200)
    keywords = models.CharField(max_length=160)
    head = models.TextField()
    scripts = models.TextField()

    class Meta():
        ordering = ['order_num']

    def __str__(self):
        return self.name


class Article (models.Model):
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    teaser_on_page = models.BooleanField(default=False)
    styles = models.TextField(blank=True)
    scripts = models.TextField(blank=True)

    class Meta():
        ordering = ['-date_created']

    def __str__(self):
        return self.title


class Feedback(models.Model):
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=80)
    user_email = models.EmailField()
    title = models.CharField(max_length=160, blank=True)
    content = models.TextField()
    teaser_on_page = models.BooleanField(default=False)

    class Meta():
        ordering = ['-date_created']

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.content[:60]


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


class Image(models.Model):
    name = models.CharField(max_length=40)
    path = models.FileField(upload_to='/images')


class ImageGallery(models.Model):
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    order_num = models.SmallIntegerField()
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    styles = models.TextField(blank=True)
    scripts = models.TextField(blank=True)

    class Meta():
        ordering = ['order_num']

    def __str__(self):
        return self.gallery_name


class ImagePlace(models.Model):
    gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE)
    order_num = models.SmallIntegerField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

    class Meta():
        unique_together = ('gallery', 'order_num')
        ordering = ['order_num']

    def __str__(self):
        return self.description


class PagePlace(models.Model):
    page = models.ForeignKey(StaticPage, on_delete=models.CASCADE, related_name='placeholder')
    order_num = models.SmallIntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True, related_name='placeholder')
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, blank=True, null=True, related_name='placeholder')
    gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE, blank=True, null=True, related_name='placeholder')

    class Meta():
        unique_together = ('page', 'order_num')
        ordering = ['order_num']

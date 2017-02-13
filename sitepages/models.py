from django.db import models

# Create your models here.

class StaticPage(models.Model):
    is_published = models.BooleanField(default=False)
    order_num = models.SmallIntegerField()
    page_name = models.CharField(max_length=30)
    page_title = models.CharField(max_length=120)
    page_description = models.CharField(max_length=200)
    page_keywords = models.CharField(max_length=160)
    page_head = models.TextField()
    page_scripts = models.TextField()

    class Meta():
        ordering = ['order_num']

    def __str__(self):
        return self.page_name


class PageArticle (models.Model):
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    article_title = models.CharField(max_length=200)
    article_content = models.TextField()
    teaser_on_page = models.BooleanField(default=False)

    class Meta():
        ordering = ['-date_created']

    def __str__(self):
        return self.article_title

    def get_page_content(self, **kwargs):
        content = self.article_content
        if self.teaser_on_page:
            pass
        return content

    def get_full_content(self, **kwargs):
        content = self.article_content
        return content


class UserFeedback(models.Model):
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=80)
    user_email = models.EmailField()
    message_title = models.CharField(max_length=160, blank=True)
    message_content = models.TextField()
    teaser_on_page = models.BooleanField(default=False)

    class Meta():
        ordering = ['-date_created']

    def __str__(self):
        if self.message_title:
            return self.message_title
        else:
            return self.message_content[:60]

    def get_page_content(self, **kwargs):
        pass

    def get_full_content(self, **kwargs):
        return self.message_content


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
    image_name = models.CharField(max_length=40)
    image_path = models.FileField(upload_to='/images')


class ImageGallery(models.Model):
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    order_num = models.SmallIntegerField()
    gallery_name = models.CharField(max_length=40)
    gallery_title = models.CharField(max_length=200, blank=True)
    gallery_description = models.TextField(blank=True)
    gallery_styles = models.TextField(blank=True)
    gallery_scripts = models.TextField(blank=True)

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
    static_page = models.ForeignKey(StaticPage, on_delete=models.CASCADE)
    place_order = models.SmallIntegerField()
    page_article = models.ForeignKey(PageArticle, on_delete=models.CASCADE, blank=True, null=True)
    user_feedback = models.ForeignKey(UserFeedback, on_delete=models.CASCADE, blank=True, null=True)
    image_gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE, blank=True, null=True)

    class Meta():
        unique_together = ('static_page', 'place_order')
        ordering = ['place_order']

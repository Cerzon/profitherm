from django.db import models

# Create your models here.

class RenderTemplate(models.Model):
    name = models.CharField(max_length=30)
    body = models.TextField()

    class Meta():
        ordering = ['name']

    def __str__(self):
        return self.name


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
        return 'From %s at %s' % (self.user_name, self.date_created)


class CalculationOrder(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=80)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=16)
    heated_area = models.PositiveSmallIntegerField()
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
    date_modified = models.DateTimeField(auto_now=True)
    order_num = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    class Meta():
        ordering = ['order_num']

    def __str__(self):
        return self.name


class Image(models.Model):
    image_gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE)
    order_num = models.PositiveSmallIntegerField()
    file_name = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=200, blank=True)

    class Meta():
        unique_together = ('image_gallery', 'order_num')
        ordering = ['order_num']

    def __str__(self):
        return self.description


class Article(models.Model):
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    teaser_on_page = models.BooleanField(default=False)
    styles = models.TextField(blank=True)
    scripts = models.TextField(blank=True)
    figures = models.ManyToManyField(ImageGallery, through='ArticleFigure')

    class Meta():
        ordering = ['-date_modified']

    def __str__(self):
        return self.title


class ArticleFigure(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    order_num = models.PositiveSmallIntegerField()
    image_gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=200, blank=True)
    styles = models.TextField(blank=True)
    scripts = models.TextField(blank=True)
    render_template = models.ForeignKey(RenderTemplate, on_delete=models.SET_NULL)

    class Meta():
        unique_together = ('article', 'order_num')
        ordering = ['order_num']

    def __str__(self):
        return self.title


class StaticPage(models.Model):
    is_published = models.BooleanField(default=False)
    order_num = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=120)
    meta_description = models.CharField(max_length=200)
    meta_keywords = models.CharField(max_length=160)
    head_tags = models.TextField()
    styles = models.TextField()
    scripts = models.TextField()
    render_template = models.ForeignKey(RenderTemplate, on_delete=models.SET_NULL)
    articles = models.ManyToManyField(Article, through='PageArticle')

    class Meta():
        ordering = ['order_num']

    def __str__(self):
        return self.name


class PageArticle(models.Model):
    static_page = models.ForeignKey(StaticPage, on_delete=models.CASCADE)
    order_num = models.PositiveSmallIntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta():
        unique_together = ('page', 'order_num')
        ordering = ['order_num']

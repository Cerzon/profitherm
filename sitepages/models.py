from django.db import models
from datetime import datetime

# Create your models here.

class DeployTemplate(models.Model):
    name = models.CharField(max_length=30)
    body = models.TextField()

    class Meta():
        ordering = ['name']

    def __str__(self):
        return self.name


class Feedback(models.Model):
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
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
    attachments = models.FileField(upload_to='uploads/calc_order/')
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
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    order_num = models.PositiveSmallIntegerField(verbose_name='Порядковый номер', help_text='Для сортировки в админке')
    name = models.CharField(max_length=80)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True, verbose_name='Общее описание иллюстрации/галереи')

    class Meta():
        ordering = ['order_num']

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.SlugField()
    file_name = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=200, blank=True)

    class Meta():
        ordering = ['name']

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    image_gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE)
    order_num = models.PositiveSmallIntegerField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    title = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta():
        unique_together = ('image_gallery', 'order_num')
        ordering = ['order_num']

    def __str__(self):
        return self.image.name


class Article(models.Model):
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    name = models.SlugField(max_length=80, unique=True, verbose_name='Имя статьи (slug)', default=datetime.today, help_text='Это название для отображения в адресной строке')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField()
    teaser_on_page = models.BooleanField(default=False, verbose_name='В списке выводить тизером', help_text='В списке объёмные статьи отображаются тизером')
    styles = models.TextField(blank=True, help_text='Можно указать несколько файлов стилей. Каждое имя файла должно быть на отдельной строке и при необходимости включать в себя путь к файлу.')
    scripts = models.TextField(blank=True, help_text='Можно указать несколько файлов скриптов. Каждое имя файла должно быть на отдельной строке и при необходимости включать в себя путь к файлу.')
    figures = models.ManyToManyField(ImageGallery, through='ArticleFigure')

    class Meta():
        ordering = ['-date_modified']
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def __str__(self):
        return self.title


class ArticleFigure(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    order_num = models.PositiveSmallIntegerField(verbose_name='Порядковый номер', help_text='Позиция отображения на странице')
    image_gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    styles = models.TextField(blank=True, help_text='Можно указать несколько файлов стилей. Каждое имя файла должно быть на отдельной строке и при необходимости включать в себя путь к файлу.')
    scripts = models.TextField(blank=True, help_text='Можно указать несколько файлов скриптов. Каждое имя файла должно быть на отдельной строке и при необходимости включать в себя путь к файлу.')
    deploy_template = models.ForeignKey(DeployTemplate, on_delete=models.SET_NULL, null=True)

    class Meta():
        unique_together = ('article', 'order_num')
        ordering = ['order_num']

    def __str__(self):
        return self.title


class StaticPage(models.Model):
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    order_num = models.PositiveSmallIntegerField(verbose_name='Порядковый номер', help_text='Для сортировки в админке')
    name = models.SlugField(max_length=80, unique=True, default=datetime.today, verbose_name='Имя статьи (slug)', help_text='Это название для отображения в адресной строке')
    title = models.CharField(max_length=120, verbose_name='Заголовок страницы', help_text='Отображается в заголовке окна браузера')
    meta_description = models.CharField(max_length=200, help_text='Содержимое параметра Content мета-тэга description')
    meta_keywords = models.CharField(max_length=160, help_text='Содержимое параметра Content мета-тэга keywords')
    head_tags = models.TextField(blank=True, help_text='HTML-тэги для размещения в разделе head страницы')
    styles = models.TextField(blank=True, help_text='Можно указать несколько файлов стилей. Каждое имя файла должно быть на отдельной строке и при необходимости включать в себя путь к файлу.')
    scripts = models.TextField(blank=True, help_text='Можно указать несколько файлов скриптов. Каждое имя файла должно быть на отдельной строке и при необходимости включать в себя путь к файлу.')
    deploy_template = models.ForeignKey(DeployTemplate, on_delete=models.SET_NULL, null=True)
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
        unique_together = ('static_page', 'order_num')
        ordering = ['order_num']

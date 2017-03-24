from django.db import models
from datetime import datetime

# Create your models here.

class DeployTemplate(models.Model):
    name = models.SlugField(max_length=50)
    body = models.TextField()

    class Meta():
        ordering = ['name']
        verbose_name = 'шаблон отображения'
        verbose_name_plural = 'шаблоны отображения'

    def __str__(self):
        return self.name


class Feedback(models.Model):
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    date_created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=120, verbose_name='Ваше имя')
    user_email = models.EmailField(verbose_name='Адрес электронной почты')
    title = models.CharField(max_length=160, blank=True, verbose_name='Тема')
    content = models.TextField(verbose_name='Сообщение')
    teaser_on_page = models.BooleanField(default=False)

    class Meta():
        ordering = ['-date_created']

    def __str__(self):
        return 'From {} at {}'.format(self.user_name, self.date_created)


class CalculationOrder(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=120, verbose_name='Контактное лицо')
    user_email = models.EmailField(verbose_name='Адрес электронной почты')
    user_phone = models.CharField(max_length=16, verbose_name='Контактный телефон')
    heated_area = models.PositiveSmallIntegerField(verbose_name='Отапливаемая площадь')
    attachments = models.FileField(upload_to='uploads/calc_order/', verbose_name='Дополнительные материалы')
    radiator_heating = models.BooleanField(default=True, verbose_name='Радиаторное отопление')
    floor_heating = models.BooleanField(default=True, verbose_name='Польное отопление')
    water_supply = models.BooleanField(default=True, verbose_name='Водоснабжение')
    water_treatment = models.BooleanField(default=False, verbose_name='Водоочистка')
    sewerage = models.BooleanField(default=True, verbose_name='Система канализации')
    boilerplant = models.BooleanField(default=True, verbose_name='Котельная/ИТП')
    svc_project = models.BooleanField(default=True, verbose_name='Проектирование')
    svc_purchase = models.BooleanField(default=True, verbose_name='Комплектация')
    svc_assembly = models.BooleanField(default=True, verbose_name='Монтаж')
    svc_reconstruction = models.BooleanField(default=True, verbose_name='Реконструкция')
    svc_maintenance = models.BooleanField(default=True, verbose_name='Сервисное обслуживание')
    svc_consulting = models.BooleanField(default=True, verbose_name='Консультация')

    class Meta():
        ordering = ['-date_created']

    def __str__(self):
        return 'Order #{} from {}'.format(self.pk, self.date_created)


class Image(models.Model):
    name = models.SlugField()
    file_name = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=200, blank=True)

    class Meta():
        ordering = ['name']
        verbose_name = 'картинка'
        verbose_name_plural = 'картинки'

    def __str__(self):
        return self.name


class ImageGallery(models.Model):
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    position = models.PositiveSmallIntegerField(verbose_name='Порядковый номер', help_text='Для сортировки в админке')
    name = models.SlugField(max_length=80)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True, verbose_name='Общее описание иллюстрации/галереи')
    styles = models.TextField(blank=True, help_text='Можно указать несколько файлов стилей. Каждое имя файла должно быть на отдельной строке и при необходимости включать в себя путь к файлу.')
    scripts = models.TextField(blank=True, help_text='Можно указать несколько файлов скриптов. Каждое имя файла должно быть на отдельной строке и при необходимости включать в себя путь к файлу.')
    deploy_template = models.ForeignKey(DeployTemplate, on_delete=models.SET_NULL, null=True, verbose_name='Шаблон отображения')

    class Meta():
        ordering = ['position']
        verbose_name = 'галерея изображений'
        verbose_name_plural = 'галереи изображений'

    def __str__(self):
        return self.name


class Figure(models.Model):
    image_gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta():
        unique_together = ('image_gallery', 'position')
        ordering = ('image_gallery', 'position')
        verbose_name = 'элемент галереи'
        verbose_name_plural = 'элементы галереи'

    def __str__(self):
        return '{} / {} / {}'.format(self.image_gallery.name, self.position, self.image.name)


class Article(models.Model):
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    name = models.SlugField(max_length=80, unique=True, verbose_name='Имя статьи (slug)', default=datetime.today, help_text='Это название для отображения в адресной строке')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(help_text='Абзацы отделяются друг от друга пустой строкой. Картинки вставлять тэгом {{ pictures.# }}, порядковые номера начиная с нуля')
    teaser_on_page = models.BooleanField(default=False, verbose_name='В списке выводить тизером', help_text='На странице объёмные статьи, обладающие собственным представлением (страницой), отображаются тизером')
    styles = models.TextField(blank=True, help_text='Можно указать несколько файлов стилей. Каждое имя файла должно быть на отдельной строке и при необходимости включать в себя путь к файлу.')
    scripts = models.TextField(blank=True, help_text='Можно указать несколько файлов скриптов. Каждое имя файла должно быть на отдельной строке и при необходимости включать в себя путь к файлу.')
    pictures = models.ManyToManyField(ImageGallery, through='ArticlePicture')

    class Meta():
        ordering = ['-date_modified']
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def __str__(self):
        return '{} / {}'.format(self.name, self.title)


class ArticlePicture(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='picturelink')
    position = models.PositiveSmallIntegerField(verbose_name='Порядковый номер', help_text='Позиция отображения на странице')
    image_gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE, related_name='picturelink')

    class Meta():
        unique_together = ('article', 'position')
        ordering = ('article', 'position')
        verbose_name = 'изображение в статье'
        verbose_name_plural = 'изображения в статье'

    def __str__(self):
        return '{} / {} / {}'.format(self.article.name, self.position, self.image_gallery.name)


class StaticPage(models.Model):
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    position = models.PositiveSmallIntegerField(verbose_name='Порядковый номер', help_text='Для сортировки в админке')
    name = models.SlugField(max_length=80, unique=True, default=datetime.today, verbose_name='Имя статьи (slug)', help_text='Это название для отображения в адресной строке')
    title = models.CharField(max_length=120, verbose_name='Заголовок страницы', help_text='Отображается в заголовке окна браузера')
    meta_description = models.CharField(max_length=200, help_text='Содержимое параметра Content мета-тэга description')
    meta_keywords = models.CharField(max_length=160, help_text='Содержимое параметра Content мета-тэга keywords')
    head_tags = models.TextField(blank=True, help_text='HTML-тэги для размещения в разделе head страницы')
    styles = models.TextField(blank=True, help_text='Можно указать несколько файлов стилей. Каждое имя файла должно быть на отдельной строке и при необходимости включать в себя путь к файлу.')
    scripts = models.TextField(blank=True, help_text='Можно указать несколько файлов скриптов. Каждое имя файла должно быть на отдельной строке и при необходимости включать в себя путь к файлу.')
    articles = models.ManyToManyField(Article, through='PageArticle')

    class Meta():
        ordering = ['position']
        verbose_name = 'страница'
        verbose_name_plural = 'страницы'

    def __str__(self):
        return self.name


class PageArticle(models.Model):
    static_page = models.ForeignKey(StaticPage, on_delete=models.CASCADE, related_name='pagelink')
    position = models.PositiveSmallIntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='pagelink')

    class Meta():
        unique_together = ('static_page', 'position')
        ordering = ('static_page', 'position')
        verbose_name = 'статья на странице'
        verbose_name_plural = 'статьи на странице'

    def __str__(self):
        return '{} / {} / {}'.format(self.static_page.name, self.position, self.article.name)

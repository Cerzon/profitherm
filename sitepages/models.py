from datetime import datetime
import os
from django.urls import reverse
from django.db import models

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
    publish_email = models.BooleanField(default=False, verbose_name='Отображать email')
    title = models.CharField(max_length=160, blank=True, default='Отзыв', verbose_name='Тема')
    content = models.TextField(verbose_name='Сообщение')

    class Meta():
        ordering = ['-date_created']
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return '{1} от {0}'.format(self.user_name, self.date_created.strftime('%d %b %Y'))


class CalculationOrder(models.Model):
    OBJECT_TYPE_CHOICES = (
        ('ctge', 'Загородный дом'),
        ('tnhs', 'Таунхаус'),
        ('flat', 'Квартира'),
    )
    date_created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=120, verbose_name='Контактное лицо')
    user_phone = models.CharField(max_length=16, verbose_name='Контактный телефон')
    user_email = models.EmailField(verbose_name='Адрес электронной почты')
    object_type = models.CharField(max_length=4, choices=OBJECT_TYPE_CHOICES, default='ctge', verbose_name='Тип объекта')
    levels_amount = models.PositiveSmallIntegerField(verbose_name='Количество этажей', default=1)
    heated_area = models.PositiveSmallIntegerField(verbose_name='Отапливаемая площадь')
    radiator_heating = models.BooleanField(default=True, verbose_name='Радиаторное отопление')
    floor_heating = models.BooleanField(default=True, verbose_name='Польное отопление')
    water_supply = models.BooleanField(default=True, verbose_name='Водоснабжение и канализация')
    water_treatment = models.BooleanField(default=False, verbose_name='Водоочистка')
    boilerplant = models.BooleanField(default=True, verbose_name='Котельная/ИТП')
    svc_project = models.BooleanField(default=True, verbose_name='Проектирование')
    svc_purchase = models.BooleanField(default=True, verbose_name='Комплектация')
    svc_assembly = models.BooleanField(default=True, verbose_name='Монтаж')
    svc_reconstruction = models.BooleanField(default=False, verbose_name='Реконструкция')
    svc_consulting = models.BooleanField(default=False, verbose_name='Консультация')
    additional_info = models.TextField(blank=True, verbose_name='Дополнительная информация')

    class Meta():
        ordering = ['-date_created']
        verbose_name = 'заказ на предварительный расчёт'
        verbose_name_plural = 'заказы на предварительный расчёт'

    def __str__(self):
        return 'Заказ #{} от {}'.format(self.pk, self.date_created.strftime('%d %b %Y'))

    def get_levels(self):
        if self.levels_amount == 1: return '1 этаж'
        if self.levels_amount in (2, 3, 4,): return str(self.levels_amount) + ' этажа'
        return str(self.levels_amount) + ' этажей'

    def get_systems(self):
        systems_list = list()
        if self.radiator_heating: systems_list.append('Радиаторное отопление')
        if self.floor_heating: systems_list.append('Тёплые полы')
        if self.water_supply: systems_list.append('Водоснабжение и канализация')
        if self.water_treatment: systems_list.append('Водоподготовка')
        if self.boilerplant: systems_list.append('Котельная')
        return systems_list

    def get_services(self):
        services_list = list()
        if self.svc_project: services_list.append('Проектирование')
        if self.svc_purchase: services_list.append('Комплектация')
        if self.svc_assembly: services_list.append('Монтаж')
        if self.svc_reconstruction: services_list.append('Реконструкция')
        if self.svc_consulting: services_list.append('Консультация')
        return services_list


def order_folder(instance, filename):
    return 'uploads/calc_order/{0}/{1}'.format(instance.calculation_order.pk, filename)


class Attachment(models.Model):
    afile = models.FileField(upload_to=order_folder, verbose_name='Дополнительные материалы')
    calculation_order = models.ForeignKey(CalculationOrder, on_delete=models.CASCADE, related_name='attachments')

    class Meta():
        ordering = ['calculation_order']
        verbose_name = 'приложение к заказу'
        verbose_name_plural = 'приложения к заказам'

    def filename(self):
        return os.path.basename(self.afile.name)

    def __str__(self):
        return 'К заказу #{0} от {1} / Файл {2}'.format(self.calculation_order.pk, self.calculation_order.date_created.strftime('%d %b %Y'), self.filename())


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
    name = models.SlugField(max_length=80, unique=True, default=datetime.today, verbose_name='Имя страницы (slug)', help_text='Это название для отображения в адресной строке')
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


class FrequentlyAskedQuestion(models.Model):
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    date_created = models.DateTimeField(auto_now_add=True)
    question_text = models.TextField(verbose_name='Развёрнутый вопрос')
    question_point = models.CharField(max_length=160, blank=True, verbose_name='Смысл вопроса (он же заголовок)')
    user_name = models.CharField(max_length=80, blank=True, verbose_name='Имя вопрошающего')
    user_email = models.EmailField(blank=True, verbose_name='Email вопрошающего')
    answer_email = models.BooleanField(default=False, verbose_name='Прислать ответ на email')
    answer_text = models.TextField(blank=True, verbose_name='Текст ответа')

    class Meta():
        ordering = ('-date_created',)
        verbose_name = 'ЧАВО'

    def __str__(self):
        return 'Вопрос от {0} / {1}'.format(self.date_created.strftime('%d %b %Y'), self.question_text[:40])

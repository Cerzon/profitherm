from django.shortcuts import get_object_or_404, render
from django.views import View
from django.template import Template, Context
from .models import Article, ArticleFigure, ArticleGallery, Image, ImageGallery, ImageGalleryItem, StaticPage, PageArticle

# Create your views here.

class ComplexPage(View):
    template = 'pages/combinepage.html'

    def get(self, request, page_name):
        # получим запрошенную страницу
        static_page = get_object_or_404(StaticPage, name=page_name)
        # списки стилей и скриптов для пополнения в дальнейшем
        styles = static_page.styles.split('\n')
        scripts = static_page.scripts.split('\n')
        # данные для шапки страницы
        title = static_page.title
        head_tags = static_page.head_tags
        meta_description = static_page.meta_description
        meta_keywords = static_page.meta_keywords
        # собираем контент
        # получить список всех статей на странице
        # цикл перебора статей страницы
            # пополнение styles и scripts стилями и скриптами статьи
            # получаем список галерей
            # если список не пустой, создаём переменную для хранения всех галерей
            # перебор прицепленных галерей статьи
                # получение данных галереи через ArticleGallery
                # пополнение styles и scripts стилями и скриптами галереи
                # создание шаблона галереи из article_gallery.render_template
                # создание контекста с данными состава галереи: image из images через ImageGalleryItem
                # рендер галереи
                # добавляем в переменную со списком галерей результаты рендера
            # получаем список иллюстраций
            # если список не пустой, создаём переменную для хранения иллюстраций
            # перебор иллюстраций
                # получение данных иллюстрации через ArticleFigure

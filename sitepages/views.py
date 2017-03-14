from django.shortcuts import get_object_or_404, render
from django.views import View
from django.template import Template, Context
from .models import Article, ArticleFigure, Image, ImageGallery, GalleryItem, StaticPage, PageArticle

# Create your views here.

class InfoPage(View):
    template = 'pages/combinepage.html'

    def get(self, request, page_name):
        # получим запрошенную страницу
        static_page = get_object_or_404(StaticPage, name=page_name)
        # списки стилей и скриптов для пополнения в дальнейшем
        styles = list()
        scripts = list()
        s = static_page.styles.strip()
        if s: styles = s.split('\r\n')
        s = static_page.scripts.strip()
        if s: scripts = s.split('\r\n')
        # данные для шапки страницы
        title = static_page.title.strip()
        head_tags = static_page.head_tags.strip()
        meta_description = static_page.meta_description.strip()
        meta_keywords = static_page.meta_keywords.strip()
        # собираем контент
        # получить список всех статей на странице
        # цикл перебора статей страницы
            # пополнение styles и scripts стилями и скриптами статьи
            # если НЕ 'показывать на странице тизер'
                # получаем список иллюстраций/галерей
                # если список не пустой, создаём переменную для хранения всех иллюстраций/галерей
                # перебор прицепленных иллюстраций/галерей статьи
                    # получение данных галереи через ArticleFigure
                    # пополнение styles и scripts стилями и скриптами галереи
                    # создание шаблона галереи из article_figure.render_template
                    # создание контекста с данными состава галереи: image из image_set
                    # рендер галереи
                    # добавляем в переменную со списком иллюстраций/галерей результаты рендера
            # создание контекста со списком рендереных иллюстраций/галлерей
            # создание шаблона из контента статьи
            # рендер статьи
            # добавляем в переменную со списком статей
        context_dict = {
            'title' : title,
            'styles' : styles,
            'scripts' : scripts,
            'head_tags' : head_tags,
            'meta_description' : meta_description,
            'meta_keywords' : meta_keywords,
            'page_content' : 'Greetings!'
            }
        return render(request, self.template, context_dict)

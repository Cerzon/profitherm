from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.db.models import Prefetch
from django.template import Template, Context
from .models import Article, ArticleFigure, Image, ImageGallery, GalleryItem, StaticPage, PageArticle

# Create your views here.

class InfoPage(View):
    template = 'pages/combinepage.html'

    def get(self, request, page_name):
        # получим запрошенную страницу
        static_page = get_object_or_404(StaticPage, name=page_name)
        if not static_page.is_published:
            raise Http404("Page does not exist or not published yet")
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
        page_articles = static_page.articles.order_by('pagelink__position')
        if page_articles:
            article_list = list()
            # цикл перебора статей страницы
            for article in page_articles:
                # пополнение styles и scripts стилями и скриптами статьи
                s = article.styles.strip()
                if s:
                    s = s.split('\r\n')
                    for si in s:
                        if not si in styles: styles.append(si)
                s = article.scripts.strip()
                if s:
                    s = s.split('\r\n')
                    for si in s:
                        if not si in scripts: scripts.append(si)
                # цикл перебора изображений/галерей в статье
        else:
            page_content = '<article><header><h2>На этой странице ничего нет</h2></header></article>'
        context_dict = {
            'title' : title,
            'styles' : styles,
            'scripts' : scripts,
            'head_tags' : head_tags,
            'meta_description' : meta_description,
            'meta_keywords' : meta_keywords,
            'page_content' : page_content,
            }
        return render(request, self.template, context_dict)

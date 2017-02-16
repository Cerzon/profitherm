from django.contrib import admin
from .models import StaticPage, Article, ArticleFigure, Image, ImageGallery, GalleryItem, DeployTemplate, PageArticle

# Register your models here.

admin.site.register(DeployTemplate)
admin.site.register(Image)
admin.site.register(ImageGallery)
admin.site.register(GalleryItem)
admin.site.register(Article)
admin.site.register(ArticleFigure)
admin.site.register(StaticPage)
admin.site.register(PageArticle)

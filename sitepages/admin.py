from django.contrib import admin
from .models import StaticPage, Article, ArticlePicture, Image, ImageGallery, Figure, DeployTemplate, PageArticle, CalculationOrder, Attachment

# Register your models here.

admin.site.register(DeployTemplate)
admin.site.register(Image)
admin.site.register(ImageGallery)
admin.site.register(Figure)
admin.site.register(Article)
admin.site.register(ArticlePicture)
admin.site.register(StaticPage)
admin.site.register(PageArticle)
admin.site.register(CalculationOrder)
admin.site.register(Attachment)

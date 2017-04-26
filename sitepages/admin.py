from django.contrib import admin
from .models import StaticPage, Article, ArticlePicture, ProfImage, ImageGallery, Figure, DeployTemplate, PageArticle, CalculationOrder, Attachment, Feedback, FrequentlyAskedQuestion

# Register your models here.

admin.site.register(DeployTemplate)
admin.site.register(ProfImage)
admin.site.register(ImageGallery)
admin.site.register(Figure)
admin.site.register(Article)
admin.site.register(ArticlePicture)
admin.site.register(StaticPage)
admin.site.register(PageArticle)
admin.site.register(CalculationOrder)
admin.site.register(Attachment)
admin.site.register(Feedback)
admin.site.register(FrequentlyAskedQuestion)

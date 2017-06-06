from django.contrib import admin
from .models import StaticPage, Article, ArticlePicture, ProfImage, ImageGallery, Figure, DeployTemplate, PageArticle, CalculationOrder, Attachment, Feedback, FrequentlyAskedQuestion

# Register your models here.

admin.site.register(ProfImage)
admin.site.register(Feedback)


class DeployTemplateAdmin(admin.ModelAdmin):
    save_as = True
admin.site.register(DeployTemplate, DeployTemplateAdmin)


class AttachmentInline(admin.StackedInline):
    model = Attachment
    extra = 0
    can_delete = False
    fields = ('afile',)
    readonly_fields = ('afile',)

    def has_add_permission(self, request, **kwargs):
        return False


class CalculationOrderAdmin(admin.ModelAdmin):
    inlines = [
        AttachmentInline,
    ]
    readonly_fields = (
        'user_name',
        'user_phone',
        'user_email',
        'object_type',
        'levels_amount',
        'heated_area',
        'radiator_heating',
        'floor_heating',
        'water_supply',
        'water_treatment',
        'boilerplant',
        'svc_project',
        'svc_purchase',
        'svc_assembly',
        'svc_reconstruction',
        'svc_consulting',
        'additional_info',
    )
    fieldsets = (
        ('Заказчик', {
            'fields': (
                'user_name',
                'user_phone',
                'user_email',
            )
        }),
        ('Объект', {
            'fields': (
                'object_type',
                'levels_amount',
                'heated_area',
            )
        }),
        ('Системы', {
            'fields': (
                'radiator_heating',
                'floor_heating',
                'water_supply',
                'water_treatment',
                'boilerplant',
            )
        }),
        ('Услуги', {
            'fields': (
                'svc_project',
                'svc_purchase',
                'svc_assembly',
                'svc_reconstruction',
                'svc_consulting',
            )
        }),
        ('Доп.материалы', {
            'fields': (
                'additional_info',
            )
        }),
    )
admin.site.register(CalculationOrder, CalculationOrderAdmin)


class FrequentlyAskedQuestionAdmin(admin.ModelAdmin):
    inlines = [
        AttachmentInline,
    ]
    readonly_fields = (
        'user_name',
        'user_email',
        'question_text',
        'answer_email',
    )
    fieldsets = (
        ('Автор', {
            'fields': (
                'user_name',
                ('user_email', 'answer_email',),
            )
        }),
        ('Вопрос', {
            'fields': (
                'question_text',
                'question_point',
            )
        }),
        ('Ответ', {
            'fields': (
                'is_published',
                'answer_text',
            )
        }),
    )
    save_on_top = True
    list_display = ('__str__', 'is_published',)
admin.site.register(FrequentlyAskedQuestion, FrequentlyAskedQuestionAdmin)


class FigureInline(admin.StackedInline):
    model = Figure


class ImageGalleryAdmin(admin.ModelAdmin):
    inlines = [
        FigureInline,
    ]
    save_on_top = True
    list_display = ('__str__', 'deploy_template', 'is_published', 'position', 'name',)
    list_display_links = ('__str__',)
    list_editable = ('deploy_template', 'position', 'name',)
admin.site.register(ImageGallery, ImageGalleryAdmin)


class ArticlePictureInline(admin.StackedInline):
    model = ArticlePicture


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        ArticlePictureInline,
    ]
    save_on_top = True
    list_display = ('__str__', 'is_published', 'name', 'title', 'teaser_on_page',)
    list_display_links = ('__str__',)
    list_editable = ('name', 'title',)
admin.site.register(Article, ArticleAdmin)


class PageArticleInline(admin.StackedInline):
    model = PageArticle


class StaticPageAdmin(admin.ModelAdmin):
    inlines = [
        PageArticleInline,
    ]
    save_on_top = True
    list_display = ('__str__', 'is_published', 'position', 'name',)
    list_display_links = ('__str__',)
    list_editable = ('position', 'name',)
admin.site.register(StaticPage, StaticPageAdmin)

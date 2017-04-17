from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.template import Template, Context
from django.views.generic.edit import CreateView
from .models import Article, ArticlePicture, Image, ImageGallery, Figure, StaticPage, PageArticle, CalculationOrder, Attachment, Feedback, FrequentlyAskedQuestion
from .forms import CalculationOrderForm, FeedbackForm, FileUploadFormSet, FrequentlyAskedQuestionForm

# Create your views here.

class InfoPage(View):
    template = 'pages/infopage.html'

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
        article_list = list()
        if page_articles:
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
                # получить список всех картинок на странице
                pictures = article.pictures.order_by('picturelink__position').select_related('deploy_template')
                picture_list = list()
                if pictures:
                    # цикл перебора картинок в статье
                    for picture in pictures:
                        # пополнение styles и scripts стилями и скриптами картинки
                        s = picture.styles.strip()
                        if s:
                            s = s.split('\r\n')
                            for si in s:
                                if not si in styles: styles.append(si)
                        s = picture.scripts.strip()
                        if s:
                            s = s.split('\r\n')
                            for si in s:
                                if not si in scripts: scripts.append(si)
                        figures = Figure.objects.filter(image_gallery=picture).order_by('position').select_related('image')
                        tpl = Template(picture.deploy_template.body)
                        ctx = Context({'figures' : figures})
                        picture_list.append(tpl.render(ctx))
                tpl = Template(article.content)
                ctx = Context({'pictures' : picture_list})
                article_body = tpl.render(ctx)
                article_list.append({
                    'title' : article.title,
                    'body' : article_body,
                    'teaser' : article.teaser_on_page,
                    'date_created' : article.date_created,
                    'date_modified' : article.date_modified
                })
        else:
            article_list = [{'title' : 'На этой странице ничего нет'}]
        context_dict = {
            'title' : title,
            'styles' : styles,
            'scripts' : scripts,
            'head_tags' : head_tags,
            'meta_description' : meta_description,
            'meta_keywords' : meta_keywords,
            'articles' : article_list,
            }
        return render(request, self.template, context_dict)


class CalculationOrderAddView(CreateView):
    form_class = CalculationOrderForm
    model = CalculationOrder
    template_name = 'pages/calculationorder_form.html'
    success_url = '/raschet-otopleniya/success/'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        upload_form = FileUploadFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, upload_form=upload_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        upload_form = FileUploadFormSet(self.request.POST, self.request.FILES)
        if (form.is_valid() and upload_form.is_valid()):
            return self.form_valid(form, upload_form)
        else:
            return self.form_invalid(form, upload_form)

    def form_valid(self, form, upload_form):
        self.object = form.save()
        upload_form.instance = self.object
        upload_form.save()
        self.request.session['order_success'] = self.object.pk
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, upload_form):
        return self.render_to_response(
            self.get_context_data(form=form, upload_form=upload_form)
        )


class CalculationOrderSuccess(View):
    template = 'pages/order_success.html'

    def get(self, request):
        if request.session.get('order_success', False):
            order = CalculationOrder.objects.select_related().get(pk=request.session['order_success'])
            del request.session['order_success']
            return render(request, self.template, {'order' : order})
        else:
            return HttpResponseRedirect('/')


class ArticleList(View):
    template = 'pages/infopage.html'

    def get(self, request):
        articles = Article.objects.filter(teaser_on_page=True)
        article_list = list()
        if articles:
            for article in articles:
                tpl = Template(article.content)
                ctx = Context({})
                article_body = tpl.render(ctx)
                article_list.append({
                    'title' : article.title,
                    'body' : article_body,
                    'teaser' : article.teaser_on_page,
                    'date_created' : article.date_created,
                    'date_modified' : article.date_modified
                })
        else:
            article_list = [{'title' : 'Статей не найдено'}]
        return render(request, self.template, {'articles' : article_list})


class FeedbackView(View):
    template = 'pages/feedback_list.html'

    def get(self, request):
        feedback_list = Feedback.objects.filter(is_published=True)
        return render(request, self.template, {'feedback_list' : feedback_list})


class FeedbackAddView(CreateView):
    form_class = FeedbackForm
    model = Feedback
    template_name = 'pages/feedback_add.html'
    success_url = '/feedback/send/'


class FeedbackSendView(View):
    template = 'pages/feedback_success.html'

    def get(self, request):
        return render(request, self.template, {})


class FrequentlyAskedQuestionListView(View):
    template = 'pages/faq_list.html'

    def get(self, request):
        faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='')
        return render(request, self.template, {'faq_list': faq_list})


class FrequentlyAskedQuestionAddView(CreateView):
    form_class = FrequentlyAskedQuestionForm
    model = FrequentlyAskedQuestion
    template_name = 'pages/faq_add.html'
    success_url = '/faq/send/'

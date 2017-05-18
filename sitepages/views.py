from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.template import Template, Context
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView, FormView
from django.core.mail import send_mail, mail_admins, mail_managers
from .models import Article, ArticlePicture, ProfImage, ImageGallery, Figure, StaticPage, PageArticle, CalculationOrder, Attachment, Feedback, FrequentlyAskedQuestion
from .forms import CalculationOrderForm, FeedbackForm, FrequentlyAskedQuestionForm, CallbackForm, CalcOrderFileUploadFormSet, QuestionFileUploadFormSet

# Create your views here.

class InfoPage(View):
    template = 'pages/infopage.html'

    def get(self, request, page_name):
        # получим запрошенную страницу
        static_page = get_object_or_404(StaticPage, name=page_name)
        if not static_page.is_published:
            raise Http404('Page does not exist or not published yet')
        # списки стилей и скриптов для пополнения в дальнейшем
        styles = set()
        scripts = set()
        # собираем контент
        # получить список всех статей на странице
        page_articles = static_page.articles.filter(is_published=True).order_by('pagelink__position')
        article_list = list()
        if page_articles:
            # цикл перебора статей страницы
            for article in page_articles:
                # пополнение styles и scripts стилями и скриптами статьи
                #styles += [style for style in article.get_styles() if style not in styles]
                #scripts += [script for script in article.get_scripts() if script not in scripts]
                styles = styles.union(article.get_styles())
                scripts = scripts.union(article.get_scripts())
                # получить список всех картинок на странице
                pictures = article.pictures.order_by('picturelink__position').select_related('deploy_template')
                if pictures:
                    picture_list = list()
                    # цикл перебора картинок в статье
                    for picture in pictures:
                        # пополнение styles и scripts стилями и скриптами картинки
                        styles = styles.union(picture.get_styles())
                        scripts = scripts.union(picture.get_scripts())
                        picture_list.append(picture.get_render())
                else:
                    picture_list = None
                tpl = Template(article.content)
                ctx = Context({'pictures' : picture_list})
                article_body = tpl.render(ctx)
                article_list.append({
                    'id' : article.id,
                    'slug' : article.name,
                    'title' : article.title,
                    'body' : article_body,
                    'teaser' : article.teaser_on_page,
                    'get_absolute_url' : article.get_absolute_url(),
                    'date_created' : article.date_created,
                    'date_modified' : article.date_modified,
                })
        else:
            article_list = None
        faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='').order_by('?')[:3]
        context_dict = {
            'page_detail' : static_page,
            'styles' : styles,
            'scripts' : scripts,
            'articles' : article_list,
            'faq_list' : faq_list,
        }
        return render(request, self.template, context_dict)


class CalculationOrderAddView(CreateView):
    form_class = CalculationOrderForm
    model = CalculationOrder
    template_name = 'pages/calculationorder_form.html'
    success_url = reverse_lazy('calculation_order_success')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        upload_form = CalcOrderFileUploadFormSet()
        page_name = reverse_lazy('calculation_order_add').split('/')[-2]
        try:
            page_detail = StaticPage.objects.get(name=page_name)
        except ObjectDoesNotExist:
            page_detail = None
        else:
            if not page_detail.is_published:
                page_detail = None
        if page_detail:
            page_articles = page_detail.articles.filter(is_published=True).order_by('pagelink__position')
            if page_articles:
                article_list = list()
                styles = set()
                scripts = set()
                for article in page_articles:
                    styles = styles.union(article.get_styles())
                    scripts = scripts.union(article.get_scripts())
                    pictures = article.pictures.order_by('picturelink__position').select_related('deploy_template')
                    if pictures:
                        picture_list = list()
                        for picture in pictures:
                            styles = styles.union(picture.get_styles())
                            scripts = scripts.union(picture.get_scripts())
                            picture_list.append(picture.get_render())
                    else:
                        picture_list = None
                    tpl = Template(article.content)
                    ctx = Context({'pictures' : picture_list})
                    article_body = tpl.render(ctx)
                    article_list.append({
                        'id' : article.id,
                        'slug' : article.name,
                        'title' : article.title,
                        'body' : article_body,
                        'teaser' : article.teaser_on_page,
                        'get_absolute_url' : article.get_absolute_url(),
                        'date_created' : article.date_created,
                        'date_modified' : article.date_modified,
                    })
            else:
                article_list = None
                styles = None
                scripts = None
        else:
            article_list = None
            styles = None
            scripts = None
        faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='').order_by('?')[:3]
        return self.render_to_response(self.get_context_data(
                page_detail=page_detail,
                articles=article_list,
                styles=styles,
                scripts=scripts,
                form=form,
                upload_form=upload_form,
                faq_list=faq_list,
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        upload_form = CalcOrderFileUploadFormSet(self.request.POST, self.request.FILES)
        if form.is_valid() and upload_form.is_valid():
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
        page_name = reverse_lazy('calculation_order_add').split('/')[-2]
        try:
            page_detail = StaticPage.objects.get(name=page_name)
        except ObjectDoesNotExist:
            page_detail = None
        else:
            if not page_detail.is_published:
                page_detail = None
        faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='').order_by('?')[:3]
        return self.render_to_response(self.get_context_data(
                page_detail=page_detail,
                form=form,
                upload_form=upload_form,
                faq_list=faq_list,
            )
        )


class CalculationOrderSuccess(View):
    template = 'pages/order_success.html'
    mail_template = 'emails/calculation_order_mail.html'

    def get(self, request):
        if request.session.get('order_success', False):
            order = CalculationOrder.objects.select_related().get(pk=request.session['order_success'])
            del request.session['order_success']
            mail_subj = 'Заказ на предварительный расчёт #{}'.format(order.pk)
            mail_msg = render_to_string(self.mail_template, {'order' : order})
            mail_managers(mail_subj, mail_msg, html_message=mail_msg)
            page_name = reverse_lazy('calculation_order_success').split('/')[-2]
            try:
                page_detail = StaticPage.objects.get(name=page_name)
                if not page_detail.is_published: page_detail = None
            except ObjectDoesNotExist:
                page_detail = None
            faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='').order_by('?')[:3]
            return render(request, self.template, {
                'page_detail' : page_detail,
                'order' : order,
                'faq_list' : faq_list,
            })
        else:
            return HttpResponseRedirect('/')


class ArticleListView(View):
    template = 'pages/infopage.html'

    def get(self, request):
        page_name = reverse_lazy('article_list').split('/')[-2]
        try:
            page_detail = StaticPage.objects.get(name=page_name)
            if not page_detail.is_published: page_detail = None
        except ObjectDoesNotExist:
            page_detail = None
        articles = Article.objects.filter(teaser_on_page=True).exclude(is_published=False)
        article_list = list()
        if articles:
            for article in articles:
                tpl = Template(article.content)
                ctx = Context({})
                article_body = tpl.render(ctx)
                article_list.append({
                    'id' : article.id,
                    'slug' : article.name,
                    'title' : article.title,
                    'body' : article_body,
                    'teaser' : article.teaser_on_page,
                    'get_absolute_url' : article.get_absolute_url,
                    'date_created' : article.date_created,
                    'date_modified' : article.date_modified,
                })
        else:
            article_list = None
        if page_detail:
            page_articles = page_detail.articles.order_by('pagelink__position')
        else:
            page_articles = None
        faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='').order_by('?')[:3]
        return render(request, self.template, {
            'page_detail' : page_detail,
            'page_articles' : page_articles,
            'articles' : article_list,
            'faq_list' : faq_list,
        })


class FeedbackListView(View):
    template = 'pages/feedback_list.html'

    def get(self, request):
        page_name = reverse_lazy('feedback_list').split('/')[-2]
        try:
            page_detail = StaticPage.objects.get(name=page_name)
            if not page_detail.is_published: page_detail = None
        except ObjectDoesNotExist:
            page_detail = None
        if page_detail:
            page_articles = page_detail.articles.order_by('pagelink__position')
        else:
            page_articles = None
        feedback_list = Feedback.objects.filter(is_published=True)
        faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='').order_by('?')[:3]
        return render(request, self.template, {
            'page_detail' : page_detail,
            'page_articles' : page_articles,
            'feedback_list' : feedback_list,
            'faq_list' : faq_list,
        })


class FeedbackAddView(CreateView):
    form_class = FeedbackForm
    model = Feedback
    template_name = 'pages/feedback_add.html'
    success_url = reverse_lazy('feedback_success')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        page_name = reverse_lazy('feedback_add').split('/')[-2]
        try:
            page_detail = StaticPage.objects.get(name=page_name)
        except ObjectDoesNotExist:
            page_detail = None
        else:
            if not page_detail.is_published:
                page_detail = None
        if page_detail:
            page_articles = page_detail.articles.filter(is_published=True).order_by('pagelink__position')
            if page_articles:
                article_list = list()
                styles = set()
                scripts = set()
                for article in page_articles:
                    styles = styles.union(article.get_styles())
                    scripts = scripts.union(article.get_scripts())
                    pictures = article.pictures.order_by('picturelink__position').select_related('deploy_template')
                    if pictures:
                        picture_list = list()
                        for picture in pictures:
                            styles = styles.union(picture.get_styles())
                            scripts = scripts.union(picture.get_scripts())
                            picture_list.append(picture.get_render())
                    else:
                        picture_list = None
                    tpl = Template(article.content)
                    ctx = Context({'pictures' : picture_list})
                    article_body = tpl.render(ctx)
                    article_list.append({
                        'id' : article.id,
                        'slug' : article.name,
                        'title' : article.title,
                        'body' : article_body,
                        'teaser' : article.teaser_on_page,
                        'get_absolute_url' : article.get_absolute_url(),
                        'date_created' : article.date_created,
                        'date_modified' : article.date_modified,
                    })
            else:
                article_list = None
                styles = None
                scripts = None
        else:
            article_list = None
            styles = None
            scripts = None
        faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='').order_by('?')[:3]
        return self.render_to_response(self.get_context_data(
                page_detail=page_detail,
                articles=article_list,
                styles=styles,
                scripts=scripts,
                form=form,
                faq_list=faq_list,
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        self.request.session['feedback_success'] = self.object.pk
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        page_name = reverse_lazy('feedback_add').split('/')[-2]
        try:
            page_detail = StaticPage.objects.get(name=page_name)
        except ObjectDoesNotExist:
            page_detail = None
        else:
            if not page_detail.is_published: page_detail = None
        faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='').order_by('?')[:3]
        return self.render_to_response(self.get_context_data(
                page_detail=page_detail,
                form=form,
                faq_list=faq_list,
            )
        )


class FeedbackSendView(View):
    template = 'pages/feedback_success.html'

    def get(self, request):
        if request.session.get('feedback_success', False):
            del request.session['feedback_success']
            mail_subj = 'Добавлен новый отзыв'
            mail_msg = 'Собственно сабж'
            mail_managers(mail_subj, mail_msg)
            page_name = reverse_lazy('feedback_success').split('/')[-2]
            try:
                page_detail = StaticPage.objects.get(name=page_name)
            except ObjectDoesNotExist:
                page_detail = None
            else:
                if not page_detail.is_published:
                    page_detail = None
            faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='').order_by('?')[:3]
            return render(request, self.template, {
                'page_detail' : page_detail,
                'faq_list' : faq_list,
            })
        else:
            return HttpResponseRedirect('/')


class FrequentlyAskedQuestionListView(View):
    template = 'pages/faq_list.html'

    def get(self, request):
        page_name = reverse_lazy('faq_list').split('/')[-2]
        try:
            page_detail = StaticPage.objects.get(name=page_name)
        except ObjectDoesNotExist:
            page_detail = None
        else:
            if not page_detail.is_published:
                page_detail = None
        if page_detail:
            page_articles = page_detail.articles.filter(is_published=True).order_by('pagelink__position')
            if page_articles:
                article_list = list()
                styles = set()
                scripts = set()
                for article in page_articles:
                    styles = styles.union(article.get_styles())
                    scripts = scripts.union(article.get_scripts())
                    pictures = article.pictures.order_by('picturelink__position').select_related('deploy_template')
                    if pictures:
                        picture_list = list()
                        for picture in pictures:
                            styles = styles.union(picture.get_styles())
                            scripts = scripts.union(picture.get_scripts())
                            picture_list.append(picture.get_render())
                    else:
                        picture_list = None
                    tpl = Template(article.content)
                    ctx = Context({'pictures' : picture_list})
                    article_body = tpl.render(ctx)
                    article_list.append({
                        'id' : article.id,
                        'slug' : article.name,
                        'title' : article.title,
                        'body' : article_body,
                        'teaser' : article.teaser_on_page,
                        'get_absolute_url' : article.get_absolute_url(),
                        'date_created' : article.date_created,
                        'date_modified' : article.date_modified,
                    })
            else:
                article_list = None
                styles = None
                scripts = None
        else:
            article_list = None
            styles = None
            scripts = None
        faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='')
        return render(request, self.template, {
            'page_detail' : page_detail,
            'styles' : styles,
            'scripts' : scripts,
            'articles' : article_list,
            'faq_list' : faq_list,
        })


class FrequentlyAskedQuestionAddView(CreateView):
    form_class = FrequentlyAskedQuestionForm
    model = FrequentlyAskedQuestion
    template_name = 'pages/faq_add.html'
    success_url = reverse_lazy('faq_success')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        upload_form = QuestionFileUploadFormSet()
        page_name = reverse_lazy('faq_add').split('/')[-2]
        try:
            page_detail = StaticPage.objects.get(name=page_name)
        except ObjectDoesNotExist:
            page_detail = None
        else:
            if not page_detail.is_published:
                page_detail = None
        if page_detail:
            page_articles = page_detail.articles.filter(is_published=True).order_by('pagelink__position')
            if page_articles:
                article_list = list()
                styles = set()
                scripts = set()
                for article in page_articles:
                    styles = styles.union(article.get_styles())
                    scripts = scripts.union(article.get_scripts())
                    pictures = article.pictures.order_by('picturelink__position').select_related('deploy_template')
                    if pictures:
                        picture_list = list()
                        for picture in pictures:
                            styles = styles.union(picture.get_styles())
                            scripts = scripts.union(picture.get_scripts())
                            picture_list.append(picture.get_render())
                    else:
                        picture_list = None
                    tpl = Template(article.content)
                    ctx = Context({'pictures' : picture_list})
                    article_body = tpl.render(ctx)
                    article_list.append({
                        'id' : article.id,
                        'slug' : article.name,
                        'title' : article.title,
                        'body' : article_body,
                        'teaser' : article.teaser_on_page,
                        'get_absolute_url' : article.get_absolute_url(),
                        'date_created' : article.date_created,
                        'date_modified' : article.date_modified,
                    })
            else:
                article_list = None
                styles = None
                scripts = None
        else:
            article_list = None
            styles = None
            scripts = None
        return self.render_to_response(self.get_context_data(
                page_detail=page_detail,
                articles=article_list,
                styles=styles,
                scripts=scripts,
                form=form,
                upload_form=upload_form,
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        upload_form = QuestionFileUploadFormSet(self.request.POST, self.request.FILES)
        if form.is_valid() and upload_form.is_valid():
            return self.form_valid(form, upload_form)
        else:
            return self.form_invalid(form, upload_form)

    def form_valid(self, form, upload_form):
        self.object = form.save()
        upload_form.instance = self.object
        upload_form.save()
        self.request.session['faq_success'] = self.object.pk
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, upload_form):
        page_name = reverse_lazy('faq_add').split('/')[-2]
        try:
            page_detail = StaticPage.objects.get(name=page_name)
        except ObjectDoesNotExist:
            page_detail = None
        else:
            if not page_detail.is_published:
                page_detail = None
        return self.render_to_response(self.get_context_data(
                page_detail=page_detail,
                form=form,
                upload_form=upload_form,
            )
        )


class FrequentlyAskedQuestionSendView(View):
    template = 'pages/faq_success.html'
    mail_template = 'emails/faq_mail.html'

    def get(self, request):
        if request.session.get('faq_success', False):
            question = FrequentlyAskedQuestion.objects.select_related().get(pk=request.session['faq_success'])
            del request.session['faq_success']
            mail_subj = 'Задан новый вопрос'
            mail_msg = render_to_string(self.mail_template, {'question' : question})
            mail_managers(mail_subj, mail_msg, html_message=mail_msg)
            page_name = reverse_lazy('faq_success').split('/')[-2]
            try:
                page_detail = StaticPage.objects.get(name=page_name)
                if not page_detail.is_published: page_detail = None
            except ObjectDoesNotExist:
                page_detail = None
            return render(request, self.template, {
                'page_detail' : page_detail
            })
        else:
            return HttpResponseRedirect('/')


class ArticleDetailView(View):
    template = 'pages/article_detail.html'

    def get(self, request, article_name):
        article = get_object_or_404(Article, name=article_name)
        if not article.is_published:
            raise Http404('Page does not exist or not published yet')
        try:
            page_detail = StaticPage.objects.get(name=article_name)
        except ObjectDoesNotExist:
            page_detail = None
        else:
            if not page_detail.is_published:
                page_detail = None
        styles = set()
        scripts = set()
        styles = styles.union(article.get_styles())
        scripts = scripts.union(article.get_scripts())
        pictures = article.pictures.order_by('picturelink__position').select_related('deploy_template')
        if pictures:
            picture_list = list()
            for picture in pictures:
                styles = styles.union(picture.get_styles())
                scripts = scripts.union(picture.get_scripts())
                picture_list.append(picture.get_render())
        else:
            picture_list = None
        tpl = Template(article.content)
        ctx = Context({'pictures' : picture_list})
        article_body = tpl.render(ctx)
        faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='').order_by('?')[:3]
        return render(request, self.template, {
            'page_detail' : page_detail,
            'styles' : styles,
            'scripts' : scripts,
            'article_title' : article.title,
            'article_body' : article_body,
            'faq_list' : faq_list,
        })


class PortfolioListView(View):
    template = 'pages/portfolio_list.html'

    def get(self, request):
        page_name = reverse_lazy('portfolio_list').split('/')[-2]
        try:
            page_detail = StaticPage.objects.get(name=page_name)
        except ObjectDoesNotExist:
            page_detail = None
        else:
            if not page_detail.is_published:
                page_detail = None
        if page_detail:
            page_articles = page_detail.articles.filter(is_published=True).order_by('pagelink__position')
            if page_articles:
                article_list = list()
                styles = set()
                scripts = set()
                for article in page_articles:
                    styles = styles.union(article.get_styles())
                    scripts = scripts.union(article.get_scripts())
                    pictures = article.pictures.order_by('picturelink__position').select_related('deploy_template')
                    if pictures:
                        picture_list = list()
                        for picture in pictures:
                            styles = styles.union(picture.get_styles())
                            scripts = scripts.union(picture.get_scripts())
                            picture_list.append(picture.get_render())
                    else:
                        picture_list = None
                    tpl = Template(article.content)
                    ctx = Context({'pictures' : picture_list})
                    article_body = tpl.render(ctx)
                    article_list.append({
                        'id' : article.id,
                        'slug' : article.name,
                        'title' : article.title,
                        'body' : article_body,
                        'teaser' : article.teaser_on_page,
                        'get_absolute_url' : article.get_absolute_url(),
                        'date_created' : article.date_created,
                        'date_modified' : article.date_modified,
                    })
            else:
                article_list = None
                styles = None
                scripts = None
        else:
            article_list = None
            styles = None
            scripts = None
        albums = ImageGallery.objects.filter(name__endswith='album', is_published=True)
        faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='').order_by('?')[:3]
        return render(request, self.template, {
            'page_detail' : page_detail,
            'articles' : article_list,
            'styles' : styles,
            'scripts' : scripts,
            'albums' : albums,
            'faq_list' : faq_list,
        })


class PortfolioDetailView(View):
    template = 'pages/portfolio_detail.html'

    def get(self, request, gallery_name):
        album = get_object_or_404(ImageGallery, name=gallery_name)
        if not album.is_published:
            raise Http404('Gallery does not exist any more or not published yet')
        styles = set()
        scripts = set()
        styles = styles.union(album.get_styles())
        scripts = scripts.union(album.get_scripts())
        try:
            page_detail = StaticPage.objects.get(name=gallery_name)
        except ObjectDoesNotExist:
            page_detail = None
        else:
            if not page_detail.is_published:
                page_detail = None
        if page_detail:
            page_articles = page_detail.articles.filter(is_published=True).order_by('pagelink__position')
            if page_articles:
                article_list = list()
                for article in page_articles:
                    styles = styles.union(article.get_styles())
                    scripts = scripts.union(article.get_scripts())
                    pictures = article.pictures.order_by('picturelink__position').select_related('deploy_template')
                    if pictures:
                        picture_list = list()
                        for picture in pictures:
                            styles = styles.union(picture.get_styles())
                            scripts = scripts.union(picture.get_scripts())
                            picture_list.append(picture.get_render())
                    else:
                        picture_list = None
                    tpl = Template(article.content)
                    ctx = Context({'pictures' : picture_list})
                    article_body = tpl.render(ctx)
                    article_list.append({
                        'id' : article.id,
                        'slug' : article.name,
                        'title' : article.title,
                        'body' : article_body,
                        'teaser' : article.teaser_on_page,
                        'get_absolute_url' : article.get_absolute_url(),
                        'date_created' : article.date_created,
                        'date_modified' : article.date_modified,
                    })
            else:
                article_list = None
        else:
            article_list = None
        faq_list = FrequentlyAskedQuestion.objects.filter(is_published=True).exclude(answer_text='').order_by('?')[:3]
        return render(request, self.template, {
            'page_detail' : page_detail,
            'articles' : article_list,
            'styles' : styles,
            'scripts' : scripts,
            'album' : album,
            'faq_list' : faq_list,
        })


class CallbackFormView(FormView):
    template_name = 'pages/callback_form.html'
    form_class = CallbackForm

    def form_valid(self, form):
        form.send_email()
        return HttpResponse('<div class="align-center">Белый конь едет вниз по кочерге, того и гляди упадёт.</div>')

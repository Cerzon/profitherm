"""profitherm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from sitepages import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.InfoPage.as_view(), {'page_name' : 'index'}),
    url(r'^articles/$', views.ArticleListView.as_view(), name='article_list'),
    url(r'^article/(?P<article_name>[\-\w]+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
    url(r'^callback/', views.CallbackFormView.as_view(), name='callback_form'),
    url(r'^faq/$', views.FrequentlyAskedQuestionListView.as_view(), name='faq_list'),
    url(r'^nashi-raboty/$', views.PortfolioListView.as_view(), name='portfolio_list'),
    url(r'^nashi-raboty/(?P<gallery_name>[\-\w]+)/$', views.PortfolioDetailView.as_view(), name='portfolio_detail'),
    url(r'^faq/question-add/$', views.FrequentlyAskedQuestionAddView.as_view(), name='faq_add'),
    url(r'^faq/question-send/$', views.FrequentlyAskedQuestionSendView.as_view(), name='faq_success'),
    url(r'^feedback/$', views.FeedbackListView.as_view(), name='feedback_list'),
    url(r'^feedback/feedback-add/$', views.FeedbackAddView.as_view(), name='feedback_add'),
    url(r'^feedback/feedback-send/$', views.FeedbackSendView.as_view(), name='feedback_success'),
    url(r'^raschet-otopleniya/$', views.CalculationOrderAddView.as_view(), name='calculation_order_add'),
    url(r'^raschet-otopleniya/order-send/$', views.CalculationOrderSuccess.as_view(), name='calculation_order_success'),
    url(r'^vodoochistka/$', views.WaterTreatmentWithRequestFormView.as_view(), name='water_treatment'),
    url(r'^vodoochistka/wtrequest-send/$', views.WaterTreatmentRequestSend.as_view(), name='wt_request_success'),
    url(r'^forms/quick-request/$', views.QuickRequestFormView.as_view(), name='quick_request_form'),
    url(r'^recaptcha-verification-failed/$', views.RecaptchaFailed.as_view(), name='recaptcha_failed'),
    url(r'^(?P<page_name>[\-\w]+)/$', views.InfoPage.as_view(), name='info_page'),
]

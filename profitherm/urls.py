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
    url(r'^articles/$', views.ArticleList.as_view(), name='article_list'),
    url(r'^raschet-otopleniya/$', views.CalculationOrderAddView.as_view(), name='calculation_order_add'),
    url(r'^raschet-otopleniya/success/$', views.CalculationOrderSuccess.as_view(), name='calculation_order_success'),
    url(r'^(?P<page_name>[\-\w]+)/$', views.InfoPage.as_view(), name='info_page'),
]

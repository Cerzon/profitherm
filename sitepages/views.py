from django.shortcuts import get_object_or_404, render
from django.views import View
from django.template import Template, Context
from .models import StaticPage, Article, ContentPlace

# Create your views here.

class ComplexPage(View):
    def get(self, request, page_name):
        static_page = get_object_or_404(StaticPage, name=page_name)
        
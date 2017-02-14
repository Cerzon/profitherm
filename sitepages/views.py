from django.shortcuts import render
from django.views import View
from .models import StaticPage, Article, ContentPlace

# Create your views here.

class ComplexPage(View):
    def get(self, request):
        pass
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import EquipmentCategory

# Create your views here.

class EquipmentMain(View):
    def get(self, request):
        return HttpResponse('А тут будет главная страница каталога')
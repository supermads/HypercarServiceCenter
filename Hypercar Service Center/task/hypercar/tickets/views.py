from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render


def welcome_view(request):
    return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "menu.html", context={})

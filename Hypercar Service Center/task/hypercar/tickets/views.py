from django.views import View
from django.http.response import HttpResponse


def welcome_view(request):
    return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')

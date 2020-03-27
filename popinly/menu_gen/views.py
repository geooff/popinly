from django.shortcuts import render


def index(request):
    return render(request, "menu_gen/index.html")

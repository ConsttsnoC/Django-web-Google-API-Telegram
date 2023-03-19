from django.shortcuts import render


def home(request):
    """
    Функция, которая возвращает домашнюю страницу.
    """
    return render(request, 'kanalservis/home.html')



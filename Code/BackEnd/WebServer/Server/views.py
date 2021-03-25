from django.shortcuts import render


def index(request):

    return render(request, 'index.html')

def prediction(request):
    return render(request, 'prediction.html')

def results(request):
    return render(request, 'results.html')



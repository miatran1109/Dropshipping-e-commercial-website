from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}
    return render(request, 'home/../home/templates/home.html', context)
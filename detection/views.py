from django.shortcuts import render

# Create your views here.

def project_list(request):
    return render(request, 'detection/home.html')


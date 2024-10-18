from django.shortcuts import render

def home(request):
    return render(request, 'tools/home.html')

def text_analysis(request):
    return render(request, 'tools/text_analysis.html')

def create_specification(request):
    return render(request, 'tools/create_specification.html')

def create_neural_network(request):
    return render(request, 'tools/create_neural_network.html')
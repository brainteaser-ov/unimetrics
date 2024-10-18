from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Database, DataObject
from .forms import DatabaseForm, DataObjectForm


def home(request):
    return render(request, 'home.html')


def database_list(request):
    databases = Database.objects.all()
    return render(request, 'databases/database_list.html', {'databases': databases})


def database_detail(request, pk):
    database = get_object_or_404(Database, pk=pk)
    data_objects = database.objects.all()
    return render(request, 'databases/database_detail.html', {'database': database, 'data_objects': data_objects})


@login_required
def create_database(request):
    if request.method == 'POST':
        form = DatabaseForm(request.POST)
        if form.is_valid():
            database = form.save(commit=False)
            database.author = request.user
            database.save()
            return redirect('database_detail', pk=database.pk)
    else:
        form = DatabaseForm()
    return render(request, 'databases/create_database.html', {'form': form})


@login_required
def add_data_object(request, pk):
    database = get_object_or_404(Database, pk=pk)
    if request.method == 'POST':
        form = DataObjectForm(request.POST, request.FILES)
        if form.is_valid():
            data_object = form.save(commit=False)
            data_object.database = database
            data_object.save()
            return redirect('database_detail', pk=pk)
    else:
        form = DataObjectForm()
    return render(request, 'databases/add_data_object.html', {'form': form, 'database': database})

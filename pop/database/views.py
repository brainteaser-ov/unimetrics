
from .utils_a import process_data
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Database, DataObject, ProcessingResult
from .forms import DatabaseForm, DataObjectForm

import logging

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html')


@login_required
def database_list(request):
    databases = Database.objects.all()
    return render(request, 'database/database_list.html', {'database': databases})


@login_required
def database_detail(request, pk):
    database = get_object_or_404(Database, pk=pk)
    data_objects = DataObject.objects.filter(database=database)

    if request.method == 'POST':
        analysis_type = request.POST.get('analysis_type')
        if analysis_type not in ['vowels', 'consonants', 'prosody']:
            messages.error(request, 'Неизвестный тип анализа.')
            return redirect('database_detail', pk=database.pk)

        for data_object in data_objects:
            result = process_data(data_object, analysis_type)
            if result:
                messages.success(request, f'Анализ "{analysis_type}" для файла {data_object.name} успешно завершен.')
            else:
                messages.error(request, f'Ошибка при анализе "{analysis_type}" файла {data_object.name}.')

        return redirect('database_detail', pk=database.pk)

    processing_results = ProcessingResult.objects.filter(data_object__in=data_objects)

    context = {
        'database': database,
        'data_objects': data_objects,
        'processing_results': processing_results,
    }
    return render(request, 'database/database_detail.html', context)


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
    return render(request, 'database/create_database.html', {'form': form})


@login_required
def add_data_object(request, pk):
    database = get_object_or_404(Database, pk=pk)
    if request.method == 'POST':
        form = DataObjectForm(request.POST, request.FILES)
        if form.is_valid():
            data_object = form.save(commit=False)
            data_object.database = database
            data_object.uploaded_by = request.user
            data_object.save()
            return redirect('database_detail', pk=database.pk)
        else:
            form = DataObjectForm()
        return render(request, 'database/add_data_object.html', {'form': form, 'database': database})

@login_required
def data_object_list(request):
    data_objects = DataObject.objects.filter(uploaded_by=request.user)
    return render(request, 'database/data_object_list.html', {'data_objects': data_objects})

@login_required
def process_selected_files(request):
    if request.method == 'POST':
        selected_files = request.POST.getlist('selected_files')
        if not selected_files:
            messages.error(request, 'Вы не выбрали ни одного файла для обработки.')
            return redirect('data_object_list')

        for object_id in selected_files:
            data_object = get_object_or_404(DataObject, pk=object_id, uploaded_by=request.user)
            # Вызов функции обработки данных
            processing_result = process_data(data_object)
            if processing_result:
                data_object.status = 'processed'
                data_object.save()
                messages.success(request, f'Файл {data_object.name} успешно обработан.')
            else:
                data_object.status = 'error'
                data_object.save()
                messages.error(request, f'Ошибка при обработке файла {data_object.name}.')
        return redirect('processing_complete')
    else:
        return redirect('data_object_list')
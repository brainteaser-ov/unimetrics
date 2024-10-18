from .forms import DatabaseForm, DataObjectForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DataObject, Database, ProcessingResult
import os
from django.core.files import File
from django.utils import timezone
from django.conf import settings
import pandas as pd
from .src.pitch_extraction import MainData
from .src.frequency import Frequency
from .src.intensity import Loudness
from .src.rate import Rate

import os
from django.core.files import File
from django.utils import timezone
from django.conf import settings
from .models import ProcessingResult


def process_data(data_object):
    try:
        file_path = data_object.file.path  # Получаем путь к аудиофайлу из DataObject
        data = MainData(file_path)
        pitch_df, intensity_df = data.get_datasets()
        frequency = Frequency(min_value=80, max_value=500, dataset=pitch_df)
        pitch_df, pitch_ratios = frequency.process_data()
        loudness = Loudness(intensity_df, min_intensity=40, max_intensity=130)
        intensity_df, intensity_ratios = loudness.process_data()
        rate = Rate(intensity_df)
        rate_df, rate_ratios = rate.process_data()
        result_filename = f"result_{data_object.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        result_directory = os.path.join(settings.MEDIA_ROOT, 'processing_results')
        os.makedirs(result_directory, exist_ok=True)
        result_filepath = os.path.join(result_directory, result_filename)

        # Сохранение результатов в один Excel-файл
        with pd.ExcelWriter(result_filepath) as writer:
            pitch_df.to_excel(writer, sheet_name='Pitch', index=False)
            pitch_ratios.to_excel(writer, sheet_name='Pitch Ratios', index=False)
            intensity_df.to_excel(writer, sheet_name='Intensity', index=False)
            intensity_ratios.to_excel(writer, sheet_name='Intensity Ratios', index=False)
            rate_df.to_excel(writer, sheet_name='Rate', index=False)
            rate_ratios.to_excel(writer, sheet_name='Rate Ratios', index=False)

        # Сохранение результата в базе данных
        with open(result_filepath, 'rb') as f:
            result_file = File(f)
            processing_result = ProcessingResult.objects.create(
                data_object=data_object,
                result_file=result_file
            )

        return processing_result

    except Exception as e:
        # Обработка ошибки
        print(f"Ошибка при обработке файла {data_object.id}: {e}")
        return None


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


@login_required
def data_object_list(request):
    data_objects = DataObject.objects.filter(uploaded_by=request.user)
    return render(request, 'database/data_object_list.html', {'data_objects': data_objects})


@login_required
def process_selected_files(request):
    if request.method == 'POST':
        selected_files = request.POST.getlist('selected_files')
        for object_id in selected_files:
            data_object = get_object_or_404(DataObject, pk=object_id, uploaded_by=request.user)
            # Вызов функции обработки данных
            processing_result = process_data(data_object)
            # Вы можете отправлять пользователю уведомления или обновлять статус объекта
        return redirect('processing_complete')
    else:
        return redirect('data_object_list')

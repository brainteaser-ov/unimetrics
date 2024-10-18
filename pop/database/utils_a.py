
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
import logging
import traceback
import logging
import traceback

logger = logging.getLogger(__name__)


def analyze_vowels(data):
    # Ваш код для анализа гласных
    vowel_df = pd.DataFrame({'placeholder': ['Результаты анализа гласных']})
    return vowel_df

def analyze_consonants(data):
    # Ваш код для анализа согласных
    consonant_df = pd.DataFrame({'placeholder': ['Результаты анализа согласных']})
    return consonant_df

def process_data(data_object, analysis_type):
    try:
        file_path = data_object.file.path  # Получаем путь к аудиофайлу
        data = MainData(file_path)
        pitch_df, intensity_df = data.get_datasets()

        result_filename = f"{analysis_type}_result_{data_object.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        result_directory = os.path.join(settings.MEDIA_ROOT, 'processing_results')
        os.makedirs(result_directory, exist_ok=True)
        result_filepath = os.path.join(result_directory, result_filename)

        # Открываем ExcelWriter
        with pd.ExcelWriter(result_filepath) as writer:
            if analysis_type == 'vowels':
                # Выполнение анализа гласных
                vowel_df = analyze_vowels(data)
                vowel_df.to_excel(writer, sheet_name='Vowels', index=False)
            elif analysis_type == 'consonants':
                # Выполнение анализа согласных
                consonant_df = analyze_consonants(data)
                consonant_df.to_excel(writer, sheet_name='Consonants', index=False)
            elif analysis_type == 'prosody':
                # Выполнение анализа просодии (ваш исходный код)
                frequency = Frequency(min_value=80, max_value=500, dataset=pitch_df)
                pitch_df, pitch_ratios = frequency.process_data()
                loudness = Loudness(intensity_df, min_intensity=40, max_intensity=130)
                intensity_df, intensity_ratios = loudness.process_data()
                rate = Rate(intensity_df)
                rate_df, rate_ratios = rate.process_data()

                # Запись результатов в Excel
                pitch_df.to_excel(writer, sheet_name='Pitch', index=False)
                pitch_ratios.to_excel(writer, sheet_name='Pitch Ratios', index=False)
                intensity_df.to_excel(writer, sheet_name='Intensity', index=False)
                intensity_ratios.to_excel(writer, sheet_name='Intensity Ratios', index=False)
                rate_df.to_excel(writer, sheet_name='Rate', index=False)
                rate_ratios.to_excel(writer, sheet_name='Rate Ratios', index=False)
            else:
                raise ValueError('Unknown analysis type')

        # Сохранение результата в базе данных
        with open(result_filepath, 'rb') as f:
            result_file = File(f)
            processing_result = ProcessingResult.objects.create(
                data_object=data_object,
                result_file=result_file,
                analysis_type=analysis_type  # Добавьте это поле в модель ProcessingResult
            )

        return processing_result

    except Exception as e:
        # Обработка ошибки
        logger.error(f"Ошибка при обработке файла {data_object.id}", exc_info=True)
        return None
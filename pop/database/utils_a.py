
import logging
import os
import traceback

import pandas as pd
import parselmouth
import textgrid
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import DatabaseForm, DataObjectForm
from .models import Database, DataObject, ProcessingResult
from .src.frequency import Frequency
from .src.intensity import Loudness
from .src.pitch_extraction import MainData
from .src.rate import Rate
from .src.formant_analysis import FormantAnalyser, FormantDataframe, FormantExtractor

logger = logging.getLogger(__name__)


def analyze_vowels(data):
    # Ваш код для анализа гласных
    vowel_df = pd.DataFrame({'placeholder': ['Результаты анализа гласных']})
    return vowel_df

def analyze_consonants(data):
    # Ваш код для анализа согласных
    consonant_df = pd.DataFrame({'placeholder': ['Результаты анализа согласных']})
    return consonant_df

def cut_audio_by_textgrid(audio_file, textgrid_file):
    sound = parselmouth.Sound(audio_file)
    tg = textgrid.TextGrid.fromFile(textgrid_file)

    output_folder = os.path.splitext(audio_file)[0] + "_split"
    os.makedirs(output_folder, exist_ok=True)

    syllables_tier = tg.getFirst('syllable')
    marks_tier = tg.getFirst('marks')

    saved_files = []

    for i, (syllable_interval, mark_interval) in enumerate(zip(syllables_tier, marks_tier)):
        syllable_name = mark_interval.mark.strip()  # Получаем название слога из слоя 'marks'

        if syllable_name:  # Проверяем, что название слога не пустое
            start_time = syllable_interval.minTime
            end_time = syllable_interval.maxTime

            sliced_sound = sound.extract_part(from_time=start_time, to_time=end_time)
            output_file = os.path.join(output_folder, f"{syllable_name}.wav")
            sliced_sound.save(output_file, "WAV")
            saved_files.append(f"{syllable_name}.wav")

    return saved_files


# def process_data(data_object, analysis_type):
#     try:
#
#         # Проверяем наличие аудиофайла и TextGrid файла
#         if not data_object.file or not data_object.annotation_file:
#             raise ValueError("Отсутствует аудиофайл или TextGrid файл у объекта.")
#
#         # Получаем пути к файлам
#         audio_file_path = data_object.file.path  # Путь к аудиофайлу
#         textgrid_file_path = data_object.annotation_file.path  # Путь к TextGrid файлу
#
#         # Разрезаем аудиофайл на слоги
#         saved_files = cut_audio_by_textgrid(audio_file_path, textgrid_file_path)
#
#         # Получаем полный путь к сохраненным файлам
#         output_folder = os.path.splitext(audio_file_path)[0] + "_split"
#         saved_file_paths = [os.path.join(output_folder, f) for f in saved_files]
#
#         # Получаем путь к аудиофайлу
#         data = MainData(saved_file_paths)
#         pitch_df, intensity_df = data.get_datasets()
#
#         result_filename = f"{analysis_type}_result_{data_object.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.xlsx"
#         result_directory = os.path.join(settings.MEDIA_ROOT, 'processing_results')
#         os.makedirs(result_directory, exist_ok=True)
#         result_filepath = os.path.join(result_directory, result_filename)
#
#         # Открываем ExcelWriter
#         with pd.ExcelWriter(result_filepath) as writer:
#             if analysis_type == 'vowels':
#                 analyser = FormantDataframe(audio_file_path, textgrid_file_path)
#
#                 # Выполняем анализ и получаем DataFrame с результатами
#                 analyzed_df = analyser.write_to_excel()
#
#                 # Записываем результаты в Excel
#                 analyzed_df.to_excel(writer, sheet_name='Vowels', index=False)
#
#             # Анализ гласных
#
#             elif analysis_type == 'consonants':
#                 # Выполнение анализа согласных
#                 consonant_df = analyze_consonants(data)
#                 consonant_df.to_excel(writer, sheet_name='Consonants', index=False)
#             elif analysis_type == 'prosody':
#                 # Выполнение анализа просодии (ваш исходный код)
#                 frequency = Frequency(min_value=80, max_value=500, dataset=pitch_df)
#                 pitch_df, pitch_ratios = frequency.process_data()
#                 loudness = Loudness(intensity_df, min_intensity=40, max_intensity=130)
#                 intensity_df, intensity_ratios = loudness.process_data()
#                 rate = Rate(intensity_df)
#                 rate_df, rate_ratios = rate.process_data()
#
#                 # Запись результатов в Excel
#                 pitch_df.to_excel(writer, sheet_name='Pitch', index=False)
#                 pitch_ratios.to_excel(writer, sheet_name='Pitch Ratios', index=False)
#                 intensity_df.to_excel(writer, sheet_name='Intensity', index=False)
#                 intensity_ratios.to_excel(writer, sheet_name='Intensity Ratios', index=False)
#                 rate_df.to_excel(writer, sheet_name='Rate', index=False)
#                 rate_ratios.to_excel(writer, sheet_name='Rate Ratios', index=False)
#             else:
#                 raise ValueError('Unknown analysis type')
#         # Сохранение результата в базе данных
#         with open(result_filepath, 'rb') as f:
#             result_file = File(f)
#             processing_result = ProcessingResult.objects.create(
#                 data_object=data_object,
#                 analysis_type=analysis_type,
#                 result_file=f'processing_results/{result_filename}'  # Используем путь относительно MEDIA_ROOT
#             )
#
#         return processing_result.result_file.url
#     except Exception as e:
#         # Обработка ошибки
#         logger.error(f"Ошибка при обработке файла {data_object.id}", exc_info=True)
#         return None

def process_data(data_object, analysis_type):
    try:
        # Проверяем наличие аудиофайла и TextGrid файла
        if not data_object.file or not data_object.annotation_file:
            raise ValueError("Отсутствует аудиофайл или TextGrid файл у объекта.")

        # Получаем пути к файлам
        audio_file_path = data_object.file.path  # Путь к аудиофайлу
        textgrid_file_path = data_object.annotation_file.path  # Путь к TextGrid файлу
        # Разрезаем аудиофайл на слоги
        saved_files = cut_audio_by_textgrid(audio_file_path, textgrid_file_path)

        # Получаем полный путь к сохраненным файлам
        output_folder = os.path.splitext(audio_file_path)[0] + "_split"
        saved_file_paths = [os.path.join(output_folder, f) for f in saved_files]
        data = MainData(saved_file_paths)
        pitch_df, intensity_df = data.get_datasets()

        result_filename = f"{analysis_type}_result_{data_object.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        result_directory = os.path.join(settings.MEDIA_ROOT, 'processing_results')
        os.makedirs(result_directory, exist_ok=True)
        result_filepath = os.path.join(result_directory, result_filename)

        # Открываем ExcelWriter
        with pd.ExcelWriter(result_filepath) as writer:
            if analysis_type == 'vowels':
                analyser = FormantDataframe(audio_file_path, textgrid_file_path)

                # Выполняем анализ и получаем DataFrame с результатами
                analyzed_df = analyser.write_to_excel()

                # Записываем результаты в Excel
                analyzed_df.to_excel(writer, sheet_name='Vowels', index=False)

            elif analysis_type == 'consonants':
                pass

            elif analysis_type == 'prosody':
                # Выполнение анализа просодии
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
                analysis_type=analysis_type,
                result_file=f'processing_results/{result_filename}'  # Используем путь относительно MEDIA_ROOT
            )

        return processing_result.result_file.url
    except Exception as e:
        # Обработка ошибки
        logger.error(f"Ошибка при обработке файла {data_object.id}", exc_info=True)
        return None

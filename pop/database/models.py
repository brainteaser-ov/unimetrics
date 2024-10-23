from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Database(models.Model):
    DATABASE_TYPES = (
        ('phonetic', 'Фонетическая'),
        ('textual', 'Текстовая'),
        ('image', 'С изображениями'),
    )
    name = models.CharField('Название базы данных', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='database', verbose_name='Автор')
    db_type = models.CharField('Тип базы данных', max_length=50, choices=DATABASE_TYPES)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.name


class DataObject(models.Model):
    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
    )

    STATUS_CHOICES = (
        ('pending', 'Не обработан'),
        ('processed', 'Обработан'),
        ('error', 'Ошибка'),
    )

    id = models.AutoField(primary_key=True)
    sequence_number = models.CharField('Порядковый номер объекта', max_length=255, blank=True, null=True)

    database = models.ForeignKey(
        Database,
        on_delete=models.CASCADE,
        related_name='data_objects',
        verbose_name='База данных'
    )
    annotation_file = models.FileField(
        upload_to='annotations/',
        blank=True,
        null=True, verbose_name='Аннотация'
    )

    name = models.CharField('Название/Описание объекта', max_length=255)
    # Список языков для выбора
    LANGUAGE_CHOICES = [
        ('русский', 'русский'),
        ('английский', 'английский'),
        ('немецкий', 'немецкий'),
        ('итальянский', 'итальянский'),
        ('испанский', 'испанский'),
        ('французский', 'французский'),
        ('кабардино-черкесский', 'кабардино-черкесский'),
        ('карачаево-балкарский', 'карачаево-балкарский'),
        ('ногайский', 'ногайский'),
        ('азербайджанский', 'азербайджанский'),
        ('осетинский', 'осетинский'),
        ('чеченский', 'чеченский'),
        ('армянский', 'армянский'),
        ('аварский', 'аварский'),
        ('кумыкский', 'кумыкский'),
    ]
    language = models.CharField(
        'Язык',
        max_length=100,
        choices=LANGUAGE_CHOICES,
        blank=True,
        null=True
    )
    text = models.TextField('Комментарий', blank=True, null=True)
    file = models.FileField('Основной файл', upload_to='files/')

    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(
        'Пол',
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    age = models.PositiveIntegerField('Возраст', blank=True, null=True)
    region = models.CharField('Регион', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        uploaded_user = self.uploaded_by
        return f"Файл {self.file.name} (загружен {uploaded_user.username})"


class FileModel(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Загрузил',
                                    related_name='uploaded_files')
    file = models.FileField('Файл', upload_to='uploads/')
    upload_date = models.DateTimeField('Дата загрузки', auto_now_add=True)

    def __str__(self):
        uploaded_user = self.uploaded_by
        return f"Файл {self.file.name} (загружен {uploaded_user.username})"


class ProcessingResult(models.Model):
    ANALYSIS_TYPES = [
        ('vowels', 'Гласные'),
        ('consonants', 'Согласные'),
        ('prosody', 'Просодия'),
    ]
    data_object = models.ForeignKey(DataObject, on_delete=models.CASCADE)
    result_file = models.FileField(upload_to='processing_results/')
    analysis_type = models.CharField(max_length=20, choices=ANALYSIS_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_analysis_type_display(self):
        return dict(self.ANALYSIS_TYPES).get(self.analysis_type, self.analysis_type)

    def __str__(self):
        return f'Результат {self.get_analysis_type_display()} для {self.data_object.name}'

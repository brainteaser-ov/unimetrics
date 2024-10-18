# database/models.py

from django.db import models
from django.contrib.auth.models import User

class Database(models.Model):
    DATABASE_TYPES = (
        ('phonetic', 'Фонетическая'),
        ('textual', 'Текстовая'),
        ('image', 'С изображениями'),
    )
    name = models.CharField('Название базы данных', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dictionaries', verbose_name='Автор')
    db_type = models.CharField('Тип базы данных', max_length=50, choices=DATABASE_TYPES)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.name

class DataObject(models.Model):
    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
    )
    database = models.ForeignKey(Database, on_delete=models.CASCADE, related_name='objects', verbose_name='База данных')
    sequence_number = models.AutoField('Порядковый номер', primary_key=True)
    name = models.CharField('Название/Описание объекта', max_length=255)
    language = models.CharField('Язык', max_length=100)
    text = models.TextField('Текст', blank=True, null=True)
    file = models.FileField('Файл', upload_to='uploads/', blank=True, null=True)
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.PositiveIntegerField('Возраст', blank=True, null=True)
    region = models.CharField('Регион', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class FileModel(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Загрузил')
    file = models.FileField('Файл', upload_to='uploads/')
    upload_date = models.DateTimeField('Дата загрузки', auto_now_add=True)

    def __str__(self):
        return f"Файл {self.file.name} (загружен {self.uploaded_by.username})"


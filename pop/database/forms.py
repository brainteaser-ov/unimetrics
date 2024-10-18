from django import forms
from .models import Database, DataObject


class DatabaseForm(forms.ModelForm):
    class Meta:
        model = Database
        fields = ['name', 'db_type']
        labels = {
            'name': 'Название базы данных',
            'db_type': 'Тип базы данных',
        }


class DataObjectForm(forms.ModelForm):
    class Meta:
        model = DataObject
        fields = ['name', 'language', 'text', 'file', 'gender', 'age', 'region', 'database']
        labels = {
            'name': 'Название/Описание объекта',
            'language': 'Язык',
            'text': 'Текст',
            'file': 'Файл',
            'gender': 'Пол',
            'age': 'Возраст',
            'region': 'Регион',
            'database': 'База данных'
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        database = self.cleaned_data.get('database')
        db_type = database.db_type if database else None

        if file and db_type:
            valid_extensions = []
            if db_type == 'phonetic':
                valid_extensions = ['.wav']
            elif db_type == 'textual':
                valid_extensions = ['.txt', '.docx']
            elif db_type == 'image':
                valid_extensions = ['.jpg', '.png']

            import os
            extension = os.path.splitext(file.name)[1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('Выберите правильный формат файла.')

        return file
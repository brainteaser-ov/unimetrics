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
        fields = ['name', 'language', 'text', 'file', 'gender', 'age', 'region']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        db_type = self.instance.database.db_type if self.instance.database else None
        labels = {
            'name': 'Название/Описание объекта',
            'language': 'Язык',
            'text': 'Текст',
            'file': 'Файл',
            'gender': 'Пол',
            'age': 'Возраст',
            'region': 'Регион',
        }

        if file and db_type:
            valid_mime_types = []
            valid_extensions = []
            if db_type == 'phonetic':
                valid_extensions = ['.wav']
            elif db_type == 'textual':
                valid_extensions = ['.txt', '.docx']
            elif db_type == 'image':
                valid_extensions = ['.jpg', '.png']

            extension = file.name[file.name.rfind('.'):].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('Выберите правильный формат файла.')

        return file
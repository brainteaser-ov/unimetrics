import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.contrib import messages


from .forms import DatabaseForm, DataObjectForm, ContactForm
from .models import Database, DataObject, ProcessingResult
from .utils_a import process_data

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html')


@login_required
def database_list(request):
    databases = Database.objects.all()
    database_count = databases.count()
    username = request.user.username
    return render(request, 'database/database_list.html', {
        'databases': databases,
        'database_count': database_count,
        'username': username
    })


@login_required
def database_detail(request, pk):
    database = get_object_or_404(Database, pk=pk)
    data_objects = database.data_objects.all()
    if request.method == 'POST':
        analysis_type = request.POST.get('analysis_type')
        if analysis_type not in ['vowels', 'consonants', 'prosody']:
            messages.error(request, 'Неизвестный тип анализа.')
            return redirect('database:database_detail', pk=database.pk)

        for data_object in data_objects:
            result = process_data(data_object, analysis_type)
            if result:
                messages.success(request, f'Анализ "{analysis_type}" для файла {data_object.name} успешно завершен.')
            else:
                messages.error(request, f'Ошибка при анализе "{analysis_type}" файла {data_object.name}.')

        return redirect('database:database_detail', pk=database.pk)

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
            return redirect('database:database_detail', pk=database.pk)
    else:
        form = DatabaseForm()
    return render(request, 'database/create_database.html', {'form': form})


@login_required
def update_database(request, pk):
    database = get_object_or_404(Database, pk=pk)
    if database.author != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = DatabaseForm(request.POST, instance=database)
        if form.is_valid():
            form.save()
            messages.success(request, 'База данных успешно обновлена.')
            return redirect('database:database_detail', pk=database.pk)
    else:
        form = DatabaseForm(instance=database)
    return render(request, 'database/update_database.html', {'form': form})


@login_required
def delete_database(request, pk):
    database = get_object_or_404(Database, pk=pk)
    if database.author != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        database.delete()
        messages.success(request, 'База данных успешно удалена.')
        return redirect('accounts:profile')
    return render(request, 'database/delete_database_confirm.html', {'database': database})


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
            return redirect('database:database_detail', pk=database.pk)
        else:
            # Если форма недействительна, мы не создаем новую форму,
            # а повторно отображаем ту же форму с ошибками
            # (данные формы уже содержат введенные пользователем данные и ошибки)
            pass  # ничего не делаем, переходим к отображению формы ниже
    else:
        # Если метод запроса не POST, создаем пустую форму
        form = DataObjectForm()

    # Отображаем форму (для метода GET и если форма недействительна при POST)
    return render(request, 'database/adddataobject.html', {'form': form, 'database': database})

@login_required
def edit_data_object(request, db_pk, pk):
    # Получаем объекты базы данных и данных
    database = get_object_or_404(Database, pk=db_pk)
    data_object = get_object_or_404(DataObject, pk=pk, database=database)

    # Проверяем права пользователя
    if database.author != request.user:
        messages.error(request, 'У вас нет прав для редактирования этого объекта.')
        return redirect('database:database_detail', pk=database.pk)

    # Обработка данных формы
    if request.method == 'POST':
        form = DataObjectForm(request.POST, request.FILES, instance=data_object)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объект успешно обновлен.')
            return redirect('database:database_detail', pk=database.pk)
    else:
        form = DataObjectForm(instance=data_object)

    # Подготовка и отображение шаблона
    context = {
        'form': form,
        'database': database,
        'data_object': data_object,
    }
    return render(request, 'database/edit_data_object.html', context)

@login_required
def delete_data_object(request, db_pk, pk):
    database = get_object_or_404(Database, pk=db_pk)
    data_object = get_object_or_404(DataObject, pk=pk, database=database)

    # Проверяем, имеет ли пользователь права на удаление
    if database.author != request.user:
        messages.error(request, 'У вас нет прав для удаления этого объекта.')
        return redirect('database:database_detail', pk=database.pk)

    if request.method == 'POST':
        data_object.delete()
        messages.success(request, 'Объект успешно удален.')
        return redirect('database:database_detail', pk=database.pk)

    context = {
        'database': database,
        'data_object': data_object,
    }

    return render(request, 'database/delete_data_object.html', context)

@login_required
def data_object_list(request):
    data_objects = DataObject.objects.filter(uploaded_by=request.user)
    return render(request, 'database/data_object_list.html', {'data_objects': data_objects})


@login_required
def process_selected_files(request, pk):
    if request.method == 'POST':
        selected_files = request.POST.getlist('selected_files')
        analysis_type = request.POST.get('analysis_type')
        if not selected_files:
            messages.error(request, 'Пожалуйста, выберите хотя бы один файл для анализа.')
            return redirect('database:database_detail', pk=pk)

        if not analysis_type:
            messages.error(request, 'Не указан тип анализа.')
            return redirect('data_object_list')

        if analysis_type not in ['vowels', 'consonants', 'prosody']:
            messages.error(request, 'Неизвестный тип анализа.')
            return redirect('data_object_list')

        if not selected_files:
            messages.error(request, 'Вы не выбрали ни одного файла для обработки.')
            return redirect('data_object_list')

        for object_id in selected_files:
            data_object = get_object_or_404(DataObject, pk=object_id, uploaded_by=request.user)
            # Вызов функции обработки данных с передачей analysis_type
            processing_result = process_data(data_object, analysis_type)
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


@login_required
def my_databases_view(request):
    databases = Database.objects.filter(author=request.user)
    database_count = databases.count()
    context = {
        'databases': databases,
        'database_count': database_count,
        'username': request.user.username,
    }
    return render(request, 'your_template.html', context)


@login_required
def database_detail(request, pk):
    database = get_object_or_404(Database, pk=pk)
    data_object_list = database.data_objects.all()
    # Пагинация
    paginator = Paginator(data_object_list, 10)  # Показывать 10 объектов на странице
    page_number = request.GET.get('page')
    data_objects = paginator.get_page(page_number)

    # Получение результатов анализа
    processing_results = ProcessingResult.objects.filter(
        data_object__in=data_object_list
    )

    # Обработка POST-запроса для запуска анализа
    if request.method == 'POST':
        analysis_type = request.POST.get('analysis_type')
        if analysis_type not in ['vowels', 'consonants', 'prosody']:
            messages.error(request, 'Неизвестный тип анализа.')
            return redirect('database:database_detail', pk=database.pk)

        for data_object in data_object_list:
            # Предполагаем, что функция process_data возвращает True или False
            result = process_data(data_object, analysis_type)
            if result:
                messages.success(request, f'Анализ "{analysis_type}" для файла {data_object.name} успешно завершен.')
            else:
                messages.error(request, f'Ошибка при анализе "{analysis_type}" файла {data_object.name}.')

    context = {
        'database': database,
        'data_objects': data_objects,
        'processing_results': processing_results,
    }
    return render(request, 'database/database_detail.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            subject = 'Новое сообщение от {}'.format(form.cleaned_data['name'])
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            recipients = ['gbshine20@gmail.com']  # Замените на ваш email

            try:
                send_mail(subject, message, sender, recipients)
                messages.success(request, 'Ваше сообщение отправлено!')
            except Exception as e:
                messages.error(request, 'Ошибка при отправке сообщения. Попробуйте позже.')

            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = ContactForm()
    return render(request, 'database/contact.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from ..database.models import Database, FileModel


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Если вы используете профиль, профиль будет создан сигналами
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    user = request.user

    # Получаем словари, созданные пользователем
    dictionaries = Database.objects.filter(author=user)

    # Получаем файлы, загруженные пользователем
    files = FileModel.objects.filter(uploaded_by=user)

    context = {
        'dictionaries': dictionaries,
        'files': files,
    }
    return render(request, 'accounts/profile.html', context)
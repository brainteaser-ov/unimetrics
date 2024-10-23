from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from database.models import Database, FileModel

from .models import Profile


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    databases = Database.objects.filter(author=user)  # Изменено
    files = FileModel.objects.filter(uploaded_by=user)  # Изменено
    if hasattr(user, 'profile'):
        profile = user.profile
    else:
        profile = None

    context = {
        'profile': profile,
        'databases': databases,
        'files': files,
    }
    return render(request, 'accounts/profile.html', context)


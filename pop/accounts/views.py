from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from database.models import Database, FileModel
from .forms import ProfileForm
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

@login_required
def file_detail(request, pk):
    file = get_object_or_404(FileModel, pk=pk, uploaded_by=request.user)
    return render(request, 'accounts/file_detail.html', {'file': file})

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})



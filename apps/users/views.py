from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('realty:catalog')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next', 'realty:catalog'))
    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('realty:catalog')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('realty:catalog')
    return render(request, 'users/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('realty:catalog')

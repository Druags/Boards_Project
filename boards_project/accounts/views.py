from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import SignUpForm

def signup(request):
    if request.method == "POST":  # если метод запроса равен POST, то начинаем проверку формы
        form = SignUpForm(request.POST)  # форма из коробки, предназначенная для создания пользователя
        if form.is_valid():  # если форма заполнена верно, то двигаемся дальше

            user = form.save()  # сохраняем пользователя в переменную
            login(request, user)  # авторизуем пользователя из созданной переменной
            return redirect('home')
    else:  # если запрос отличается от POST, то создаём пустую форму
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


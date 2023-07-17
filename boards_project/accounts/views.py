from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

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


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
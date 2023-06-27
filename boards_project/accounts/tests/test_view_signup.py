from django.urls import resolve, reverse
from django.test import TestCase
from rest_framework.authtoken.admin import User

from ..forms import SignUpForm
from ..views import signup


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')  # через имя вьюшки получаем ссылку, по которой она вызывается
        self.response = self.client.get(url)

    def test_signup_status_code(self):  # проверка того, что страница исправно открывается
        url = reverse('signup')  # через имя вьюшки получаем ссылку, по которой она вызывается
        response = self.client.get(url)  # получаем результат обращения по ссылке из переменной url
        self.assertEquals(response.status_code, 200)  # сравниваем статус-код результата с кодом 200

    def test_signup_url_resolves_signup_view(self):  # проверка того, что переход по ссылке возвращает нужную вьюшку
        view = resolve('/signup/')  # получаем вьюшку, которая возвращается по этой ссылке
        self.assertEquals(view.func, signup)  # сравниваем полученную вьюшку с заранее известной

    def test_csrf(self):  # проверка csrf-токена
        self.assertContains(self.response, 'csrfmiddlewaretoken')  # проверяем, что в запросе есть токен

    def test_contains_form(self):  # проверка наличия формы в запросе
        form = self.response.context.get('form')  # получаем из контекста ответа форму
        self.assertIsInstance(form, SignUpForm)  # сравниваем полученную форму с искомой

    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to the home page
        '''
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())

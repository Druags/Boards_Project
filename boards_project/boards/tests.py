from django.test import TestCase
from django.urls import reverse, resolve


# Create your tests here.
from .views import home_view


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        print(1,url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        print(2, view, resolve('/admin/'))
        self.assertEquals(view.func, home_view)
from django.test import TestCase
from django.urls import reverse, resolve


# Create your tests here.
from .views import home_view, board_topics_view
from .models import Board

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


class BoardTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse(board_topics_view, kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse(board_topics_view, kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1')
        self.assertEquals(view.func, board_topics_view)
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import News
# Create your tests here.

User = get_user_model()

class NewsTest(TestCase):
    def setUp(self):
        admin_user = User(username='admin', email='admin@admin.com')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password('admin')
        admin_user.save()
        self.admin = admin_user
        self.admin_name = 'admin'
        self.admin_password = 'admin'
        registered_user = User(username='registered', email='registered@registered.com')
        registered_user.is_staff = False
        registered_user.is_superuser = False
        registered_user.set_password('registered')
        registered_user.save()
        self.registered = registered_user
        self.registered_name = 'registered'
        self.registered_password = 'registered'
        n1 = News.objects.create(
            author=self.admin,
            article='news gaaaaaaa',
            body='body gaaaaaaaa'
        )

    def test_setup_user_count(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)

    def test_all_access_view(self):
        admin_login = self.client.login(username=self.admin_name, password=self.admin_password)
        response = self.client.get(reverse('detail-news', args=(1,)))
        self.assertTrue(response.status_code==200)
    
    def test_forbidden_regular_access_view(self):
        self.client.login(username=self.registered_name, password=self.registered_password)
        response = self.client.post('/news/create/', {'article': 'denied'})
        # /news/create -> /news/create/ Добавил / и все заработало=)
        self.assertTrue(response.status_code==403)
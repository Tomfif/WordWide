from django.test import TestCase

from django import urls
from django.contrib.auth import get_user_model, authenticate
import pytest
from django.contrib.auth.models import User


from WWapp.models import Story, Rating


@pytest.mark.parametrize('param', [
    ('home'),
    ('stories'),
    ('mystories'),
    ('add-user'),
    ('login-user'),
    ('logout-user'),

])
@pytest.mark.django_db
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 302 or 200


@pytest.mark.django_db
def test_user_signup(client, user_data):
    user_model = get_user_model()
    assert user_model.objects.count() == 0
    signup_url = urls.reverse('add-user')
    resp = client.post(signup_url, user_data, Follow=True)
    assert user_model.objects.count() == 1
    assert resp.status_code == 302


class SigninTest(TestCase):
    @pytest.mark.django_db
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='test', email='test@example.com')
        self.user.save()

    @pytest.mark.django_db
    def tearDown(self):
        self.user.delete()

    @pytest.mark.django_db
    def test_correct(self):
        user = authenticate(username='test', password='test')
        self.assertTrue((user is not None) and user.is_authenticated)

    @pytest.mark.django_db
    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    @pytest.mark.django_db
    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


@pytest.mark.django_db
def test_user_created(create_test_user):
    user_model = get_user_model()
    assert user_model.objects.count() == 1


@pytest.mark.django_db
def test_user_login(client, create_test_user, user_data):
    user_model = get_user_model()
    assert user_model.objects.count() == 1
    login_url = urls.reverse('login-user')
    resp = client.post(login_url, data=user_data)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_user_login(client):
    login_url = urls.reverse('login-user')
    resp = client.post(login_url, data={'login': 'tomek', 'password': 'tomek'})
    assert resp.status_code == 200


class LogInTest(TestCase):
    @pytest.mark.django_db
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    @pytest.mark.django_db
    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)


@pytest.mark.django_db
def test_logout(client):
    client.login(user='aga', password='aga')
    url = '/logout/'
    response = client.get(url, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_modifystory_ok(client, story):
    user = User.objects.create(username='user', password='user')
    user.save()
    client.force_login(user=user)
    url = f'/modifystory/{story.id}/'
    response = client.get(url, Follow=True)
    assert response.status_code == 200
    assert Story.objects.get(title="tytul11") == story
    assert str(story.genre) == 'Biography'
    assert response.context['story'].world.world == 2


@pytest.mark.django_db
def test_story_has_an_author(create_test_user, genre, hero, world):
    story = Story.objects.create(title='tytul11', author=create_test_user, genre=genre, hero=hero, world=world)
    assert story.title == 'tytul11'


@pytest.mark.django_db
def test_storydetails_ok(client, story):
    url = f'/story_details/{story.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert str(story.world) == 'Westeros from A Game of Thrones'
    assert response.context['story'].title == 'tytul11'


@pytest.mark.django_db
def test_rating_ok(client, rating, story):
    url = f'/rating/{story.id}/'
    response = client.post(url)
    assert response.status_code == 200
    assert Rating.objects.count() == 1


@pytest.mark.django_db
def test_deletestory(client, story):
    assert Story.objects.count() == 1
    user = User.objects.create(username='user', password='user')
    user.save()
    client.force_login(user=user)
    url = f'/deletestory/{story.id}'
    response = client.post(url, follow=True)
    assert response.status_code == 200
    assert Story.objects.count() == 0


@pytest.mark.django_db
def test_stories(client, stories):
    url = f'/stories/'
    response = client.get(url)
    assert response.status_code == 200
    assert Story.objects.count() == 3
    assert response.context['object_list'][1].title == 'tytul22'


@pytest.mark.django_db
def test_my_stories(client):
    url = f'/mystories/'
    response = client.get(url, follow=True)
    assert response.status_code == 404
    username = 'test_user'
    password = 'test_pass'
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    url = f'/mystories/'
    response = client.get(url, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_storydrawn(client):
    user = User.objects.create_user(username='tt', password='tt')
    user.save()
    client.force_login(user=user)
    assert Story.objects.count() == 0
    url = f'/storydrawn/'
    response = client.get(url)
    assert response.status_code == 200
    assert Story.objects.count() == 1


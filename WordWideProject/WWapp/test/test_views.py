from unittest import TestCase


from django import urls
from django.contrib.auth import get_user_model, authenticate
import pytest
from django.contrib.auth.models import User
from django.urls import reverse

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
    resp = client.post(signup_url, user_data)
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

class SignInViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test',
                                                         password='12test12',
                                                         email='test@example.com')


    @pytest.mark.django_db
    def test_correct(self):
        response = self.client.post('/register/', {'username': 'test', 'password': '12test12'})
        self.assertTrue(response.data['authenticated'])

    @pytest.mark.django_db
    def test_wrong_username(self):
        response = self.client.post('/register/', {'username': 'wrong', 'password': '12test12'})
        self.assertFalse(response.data['authenticated'])

    @pytest.mark.django_db
    def test_wrong_pssword(self):
        response = self.client.post('/register/', {'username': 'test', 'password': 'wrong'})
        self.assertFalse(response.data['authenticated'])




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
    resp = client.post(login_url, data={'login':'tomek', 'password':'tomek'})
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
def test_modifystory_ok(client, story):
    url = f'/modifystory/{story.id}'
    response = client.get(url)
    assert response.status_code == 301
    assert Story.objects.get(title="tytul11") == story

@pytest.mark.django_db
def test_story_has_an_author(create_test_user, genre, hero, world):
    story = Story.objects.create(title='tytul11', author=create_test_user, genre=genre, hero=hero, world=world)
    assert story.title == 'tytul11'

@pytest.mark.django_db
def test_storydetails_ok(client, create_test_user, genre, hero, world):
    story = Story.objects.create(title='tytul11', author=create_test_user, genre=genre, hero=hero, world=world)
    url = f'/story_details/{story.id}'
    response = client.get(url)
    assert response.status_code == 301
    assert str(story.world) == 'Westeros from A Game of Thrones'

@pytest.mark.django_db
def test_rating_ok(client, create_test_user, genre, hero, world):
    story = Story.objects.create(title='tytul11', author=create_test_user, genre=genre, hero=hero, world=world)
    rating = Rating.objects.create(comment='komentarz', stars='3', story=story, nick='losowy')
    url = f'/rating/{rating.id}'
    response = client.get(url)
    assert response.status_code == 301
    assert str(rating.comment) == 'komentarz'

@pytest.mark.django_db
def test_deletestory(client, create_test_user, genre, hero, world):
    story = Story.objects.create(title='tytul11', author=create_test_user, genre=genre, hero=hero, world=world)
    assert Story.objects.count() == 1
    user = User.objects.create(username='user', password='user')
    user.save()
    client.force_login(user=user)
    url = f'/deletestory/{story.id}'
    response = client.get(url)
    assert response.status_code == 301
    assert Story.objects.count() == 0


@pytest.mark.django_db
def test_my_stories(client, create_test_user, genre, hero, world):
    story = Story.objects.create(title='tytul11', author=create_test_user, genre=genre, hero=hero, world=world)
    story2 = Story.objects.create(title='tytul22', author=create_test_user, genre=genre, hero=hero, world=world)
    story3 = Story.objects.create(title='tytul33', author=create_test_user, genre=genre, hero=hero, world=world)


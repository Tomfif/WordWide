from django import urls
from django.contrib.auth import get_user_model
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
    resp = client.post(signup_url, user_data)
    assert user_model.objects.count() == 1
    assert resp.status_code == 302

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
    resp = client.post(login_url, data={'login':'tomek', 'password':'tom'})
    assert resp.status_code == 200
    # assert 'tomek' in str(resp.content)

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
    rating = Rating.objects.create(comment='komentarz', stars='3', story=story, user=create_test_user)
    url = f'/rating/{rating.id}'
    response = client.get(url)
    assert response.status_code == 301
    assert str(rating.comment) == 'komentarz'

@pytest.mark.django_db
def test_deletestory(client, create_test_user, genre, hero, world):
    story = Story.objects.create(title='tytul11', author=create_test_user, genre=genre, hero=hero, world=world)
    assert Story.objects.count() == 1
    url = f'/deletestory/{story.id}'
    response = client.get(url)
    assert response.status_code == 301
    assert Story.objects.count() == 0
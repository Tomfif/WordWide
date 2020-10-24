import pytest
from django.contrib.auth import get_user_model

from WWapp.models import Genre, World, Title, Hero, Story, Rating
from django.test import Client


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user_data():
    return {'mail': 'user_email@wp.pl', 'first_name': 'name1', 'last_name': 'name2',
            'username': 'usernnname1', 'password1': 'pas1', 'password2': 'pas1'}


@pytest.fixture
def create_test_user(user_data):
    user_model = get_user_model()
    test_user = user_model.objects.create_user(user_data)
    return test_user


@pytest.fixture
def world():
    world = World.objects.create(world=2)
    return world


@pytest.fixture
def genre():
    genre = Genre.objects.create(genre=1)
    return genre


@pytest.fixture
def title():
    title = Title.objects.create(title='Swiat1')
    return title


@pytest.fixture
def hero():
    hero = Hero.objects.create(name='Imie1', intelligence='50', strength='50', speed='50', durability='50',
                               biography='biog1', alteregos='aletr1', gender='gender1', race='rasa1',
                               occupation='zawod',
                               image='zdjecie1')
    return hero


@pytest.fixture
def story(create_test_user, genre, hero, world):
    story = Story.objects.create(title='tytul11', author=create_test_user, genre=genre, hero=hero, world=world)
    return story


@pytest.fixture
def rating():
    rating = Rating.objects.create(comment='komentarz1', stars='3', story='opow1', user='user1')
    return rating


@pytest.fixture
def stories(create_test_user, genre, hero, world):
    story = Story.objects.create(title='tytul11', author=create_test_user, genre=genre, hero=hero, world=world)
    story2 = Story.objects.create(title='tytul22', author=create_test_user, genre=genre, hero=hero, world=world)
    story3 = Story.objects.create(title='tytul33', author=create_test_user, genre=genre, hero=hero, world=world)
    return Story.objects.all()

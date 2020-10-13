import pytest



from WWapp.models import Genre, World, Title, Hero, Story, Rating


@pytest.fixture
def world():
    world = World.objects.create(world='Swiat1')
    return world

@pytest.fixture
def genre():
    genre = Genre.objects.create(genre='Gatunek1')
    return genre

@pytest.fixture
def title():
    title = Title.objects.create(title='Swiat1')
    return title

@pytest.fixture
def hero():
    hero = Hero.objects.create(name='Imie1', intelligence='50', strength='50', speed='50', durability='50',
                               biography='biog1', alteregos='aletr1', gender='gender1', race='rasa1', occupation='zawod',
                               image='zdjecie1')
    return hero

@pytest.fixture
def story():
    story = Story.objects.create(title='tytul11', author='autor', genre='genre11', hero='bohater1', world='swiat111')
    return story

@pytest.fixture
def rating():
    rating = Rating.objects.create(comment='komentarz1', stars='3', story='opow1', user='user1')
    return rating


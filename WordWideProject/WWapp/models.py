from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField

GENRE_CHOICES = (
    (-1, 'not defined'),
    (0, 'Journalism' ),
    (1, 'Biography'),
    (2, 'Western'),
    (3, 'Travel'),
    (4, 'Tragicomedy '),
    (5, 'Suspense/thriller'),
    (6, 'Theological fiction'),
    (7, 'Swashbuckler '),
    (8, 'Spy fiction'),
    (9, 'Science fiction '),
    (10, 'Satire '),
    (11, 'Romance'),
    (12, 'Mythology '),
    (13, 'Magical realism '),
    (14, 'Legend '),
    (15, 'Humor'),
    (16, 'Horror'),
    (17, 'Historical fiction  '),
    (18, 'Fantasy '),
    (19, 'Epic  '),
    (20, 'Crime/detective '),
    (21, 'Legend '),
)
STARS_CHOICES = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
    (6, "6"),
    (7, "7"),
    (8, "8"),
    (9, "9"),
    (10, "10"),
)

WORLD_CHOICES = (
    (-1, 'not defined'),
    (0, 'Middle-Earth from The Lord of the Rings' ),
    (1, 'Narnia from The Chronicles of Narnia'),
    (2, 'Westeros from A Game of Thrones'),
    (3, 'The Unnamed Land in Robert Jordan’s Wheel of Time'),
    (4, 'The Land of Oz from The Wizard of Oz '),
    (5, 'Dinotopia by James Gurney'),
    (6, 'Earthsea from A Wizard of Earthsea'),
    (7, 'Hogwarts from the Harry Potter series '),
    (8, 'Wonderland from Alice’s Adventures in Wonderland'),
    (9, 'Neverland from Peter Pan'),
)


TITLE_CHOICES = (
    (-1, 'not defined'),
    (0, 'Rings'),
    (1, "The Fall of The Orb"),
    (2, "The Voice of the Heir"),
    (3, "The Specter in the Vale"),
    (4, "Sign of the Crooked Cottage"),
    (5, "Babylon Grieving"),
    (6, "Sword`s Voyage"),
    (7, "Clue of the Split Amulet"),
    (8, "Bam Went My Heart"),
    (9, "The Spell in the Dusk"),
    (10, "Wet Wild Winter"),
)

class Genre(models.Model):
    genre = models.SmallIntegerField(choices=GENRE_CHOICES, default=-1)

    def __str__(self):
        return self.get_genre_display()


class World(models.Model):
    world = models.SmallIntegerField(choices=WORLD_CHOICES, default=-1)

    def __str__(self):
        return self.get_world_display()


class Title(models.Model):
    title = models.SmallIntegerField(choices=TITLE_CHOICES, default=-1)

    def __str__(self):
        return self.get_title_display()


class Hero(models.Model):
    name = models.CharField(max_length=200, null=True)
    intelligence = models.CharField(max_length=200, null=True)
    strength = models.CharField(max_length=200, null=True)
    speed = models.CharField(max_length=200, null=True)
    durability = models.CharField(max_length=200, null=True)
    biography = models.CharField(max_length=200, null=True)
    alteregos = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, null=True)
    race = models.CharField(max_length=200, null=True)
    occupation = models.CharField(max_length=200, null=True)
    image = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

class Story(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    content = RichTextField(default="", blank=True, null=True)

    def __str__(self):
        return f'{self.author} {self.title} {self.genre.get_genre_display()} {self.hero} {self.world}'


class Rating(models.Model):
    comment = models.TextField(default="", blank=True, null=True)
    stars = models.PositiveIntegerField(choices=STARS_CHOICES, default=5)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    nick = models.CharField(max_length=250, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


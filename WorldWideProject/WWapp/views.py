from django.shortcuts import render, redirect, get_object_or_404
from random import random, randint

import requests
from django.views import View

from WWapp.models import Hero, Genre, World, Story



class StoryDrawnView(View):
    def get(self, request):
        rnd_hero = randint(1, 731)
        rnd_genre = randint(0, 21)
        rnd_world = randint(0, 9)
        url = 'https://superheroapi.com/api/5072836502742329/'
        new_url = "{}/{}".format(url, rnd_hero)
        response = requests.get(new_url)
        data_hero = response.json()
        name = data_hero['name']
        intelligence = data_hero['powerstats']['intelligence']
        strength = data_hero['powerstats']['strength']
        speed = data_hero['powerstats']['speed']
        durability = data_hero['powerstats']['durability']
        full_name = data_hero['biography']['full-name']
        alteregos = data_hero['biography']['alter-egos']
        gender = data_hero['appearance']['gender']
        race = data_hero['appearance']['race']
        occupation = data_hero['work']['occupation']
        image = data_hero['image']['url']
        hero = Hero.objects.create(name=name, intelligence=intelligence, strength=strength, speed=speed, durability=durability,
                                   biography=full_name, alteregos=alteregos, gender=gender, race=race, occupation=occupation,
                                   image=image)
        genre = Genre.objects.create(genre=rnd_genre)
        world = World.objects.create(world=rnd_world)

        return render(request, "storydrawn.html", context={"hero": hero, "genre": genre, "world": world})

    def post(self, request):
        title = request.POST.get('title')
        hero = request.POST.get('hero')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        world = request.POST.get('world')
        story = Story.objects.create(title=title, hero=hero, author=author, genre=genre, world=world)
        return redirect(f'/story/modify/{story.id}/')


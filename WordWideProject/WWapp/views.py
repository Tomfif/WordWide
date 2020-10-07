from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from random import random, randint

import requests
from django.views import View

from WWapp.models import Hero, Genre, World, Story, Title
from django.views.generic import ListView, UpdateView, DetailView, FormView

from WWapp.forms import AddUserForm, LoginUserForm, StoryForm



class StoryDrawnView(View):
    def get(self, request):
        rnd_hero = randint(1, 731)
        rnd_genre = randint(0, 21)
        rnd_world = randint(0, 9)
        rnd_title = randint(0, 10)
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
        title = Title.objects.create(title=rnd_title)

        story = Story.objects.create(title=title, hero=hero, genre=genre, world=world, author=self.request.user)

        return render(request, "storydrawn.html", context={"hero": hero, "genre": genre, "world": world, "story": story})

    # def post(self, request):
    #     title = request.POST.get('title')
    #     hero = request.POST.get('hero')
    #     author = request.POST.get('author')
    #     genre = request.POST.get('genre')
    #     world = request.POST.get('world')
    #     story = Story.objects.create(title=title, hero=hero, author=author, genre=genre, world=world)
    #     return redirect(f'/story/modify/{story.id}/')

class LandingView(View):
    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "landing_page.html", ctx)

class StoriesListView(ListView):
    template_name = 'stories_list.html'
    model = Story

class StoryUpdate(UpdateView):
    model = Story
    form_class = StoryForm
    success_url = "/"

class StoryDetailsView(DetailView):
    model = Story
    template_name = 'story_details_view.html'


class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'add_user.html', {'form': form})
    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return HttpResponse("Użytkownik z takim loginiem juz istnieje")
            else:
                user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email=form.cleaned_data['mail'],
                                                password=form.cleaned_data['password1'])
                user.last_name = form.cleaned_data['last_name']
                user.first_name = form.cleaned_data['first_name']
                user.save()
                return redirect('/')
        return render(request, 'add_user.html', {'form': form})

class LoginUserView(FormView):
    template_name = 'login_user.html'
    form_class = LoginUserForm
    success_url = '/'
    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
        else:
            return HttpResponse("Invalid User")
        return super(LoginUserView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponse("Logged out")

class MyStoriesListView(ListView):
    template_name = 'my_stories_list.html'
    model = Story



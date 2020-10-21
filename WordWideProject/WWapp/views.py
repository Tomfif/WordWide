from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from random import random, randint

import requests
from django.views import View

from WWapp.models import Hero, Genre, World, Story, Title, Rating
from django.views.generic import ListView, UpdateView, DetailView, FormView, CreateView, DeleteView

from WWapp.forms import AddUserForm, LoginUserForm, StoryForm, RatingForm


class StoryDrawnView(View):
    def get(self, request):
        """View that randomizes the basic data for the story, such as the world, hero, title, genre."""
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

class LandingView(View):
    def get(self, request):
        """View that renders the home page."""
        ctx = {"actual_date": datetime.now()}
        return render(request, "landing_page.html", ctx)

class StoriesListView(ListView):
    """View that renders the stories list.
        The view is also available for non-logged in users"""
    template_name = 'stories_list.html'
    model = Story
    ordering = ['-date_added']
    paginate_by = 10

class StoryUpdate(UpdateView):
    """View in which you write or modify the story"""
    model = Story
    form_class = StoryForm
    success_url = "/"

class StoryDetailsView(DetailView):
    """View that renders the story details."""
    model = Story
    template_name = 'story_details_view.html'

    def get_context_data(self, **kwargs):
        """method that returns all grades for a given story"""
        context = super(StoryDetailsView, self).get_context_data(**kwargs)
        context['ratings'] = Rating.objects.filter(story_id=self.object.id).all()
        return context


class AddUserView(View):
    """user registration view"""
    def get(self, request):
        """form rendering method"""
        form = AddUserForm()
        return render(request, 'add_user.html', {'form': form})
    def post(self, request):
        """method that validates the form and creates a user"""
        form = AddUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return HttpResponse("User already exists")
            else:
                user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email=form.cleaned_data['mail'],
                                                password=form.cleaned_data['password1'])
                user.last_name = form.cleaned_data['last_name']
                user.first_name = form.cleaned_data['first_name']
                user.save()
                return redirect('/mystories')
        return render(request, 'add_user.html', {'form': form})

class LoginUserView(FormView):
    """user login view"""
    template_name = 'login_user.html'
    form_class = LoginUserForm
    success_url = '/'
    def form_valid(self, form):
        """method that validates the form and login a user"""
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
        else:
            return redirect('/')
        return super(LoginUserView, self).form_valid(form)


class LogoutView(View):
    """user logout view"""
    def get(self, request):
        logout(request)
        return redirect('/')

class MyStoriesListView(LoginRequiredMixin, ListView):
    """View that renders the current user stories list.
            The view is available for logged in users"""
    template_name = 'my_stories_list.html'
    model = Story
    redirect_field_name = "/404"
    paginate_by = 10
    def get_queryset(self):
        """method of filtering stories of logged in user"""
        user = self.request.user
        return Story.objects.filter(author=user)



class RatingCreate(CreateView):
    """view that creates the rating"""
    model = Rating
    form_class = RatingForm
    success_url = "/stories/"


    # def get_initial(self):
    #     story = get_object_or_404(Story, id=self.kwargs.get('id'))
    #     return {
    #         'story': story,
    #     }

    # def get_context_data(self, **kwargs):
    #     ctx = super(RatingCreate, self).get_context_data(**kwargs)
    #     ctx['story'] = Story.objects.filter(pk=self.kwargs.get('pk'))
    #     return ctx
    # def get_queryset(self):
    #     story = self.request.story
    #     return Story.objects.filter(story=story)



class DeleteStory(DeleteView):
    """view that deletes the story of a logged in user"""
    template_name = 'delete_story.html'
    success_url = "/mystories/"
    model = Story
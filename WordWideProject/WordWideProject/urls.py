"""WordWideProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from WWapp.views import StoryDrawnView, LandingView, StoriesListView, StoryUpdate, StoryDetailsView, AddUserView, LoginUserView, LogoutView

from WWapp.views import MyStoriesListView, RatingCreate, DeleteStory



urlpatterns = [
    path('admin/', admin.site.urls),
    path('storydrawn/', StoryDrawnView.as_view(), name='storydrawn'),
    path('', LandingView.as_view(), name='home'),
    path('stories/', StoriesListView.as_view(), name='stories'),
    path('modifystory/<int:pk>/', StoryUpdate.as_view()),
    path('story_details/<int:pk>/', StoryDetailsView.as_view()),
    path('register/', AddUserView.as_view(), name="add-user"),
    path('login/', LoginUserView.as_view(), name="login-user"),
    path('logout/', LogoutView.as_view(), name="logout-user"),
    path('mystories/', MyStoriesListView.as_view(), name='mystories'),
    path('rating/<int:pk>/', RatingCreate.as_view()),
    path('deletestory/<int:pk>/', DeleteStory.as_view()),
]

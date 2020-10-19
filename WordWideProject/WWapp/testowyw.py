import pytest
from django.test import TestCase

from WWapp.models import Story



@pytest.mark.django_db
def Test_story_drawn_ok(client):
    response = client.get('storydrawn/')
    assert response.status_code == 200
    assert Story.objects.count() ==1





@pytest.mark.django_db
def Test_modifystory_ok(client, story):
    url = f'/modifystory/{story.id}'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['title'] == 'tytul11'




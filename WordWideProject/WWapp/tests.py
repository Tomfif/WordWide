import pytest
from django.test import TestCase

from WWapp.models import Story


class TestViews(TestCase):
    @pytest.mark.django_db
    def Test_story_drawn_ok(self, story):
        response = self.client.get('storydrawn/')
        assert response.status_code == 200
        assert Story.objects.count() ==1





    @pytest.mark.django_db
    def Test_modifystory_ok(self, story):
        url = f'/modifystory/{story.id}'
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.context['title'] == 'tytul11'




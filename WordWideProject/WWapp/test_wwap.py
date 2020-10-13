from django.test import TestCase

class TestViews(TestCase):
    def Test_story_drawn_ok(self):
        response = self.client.get('storydrawn/')
        assert response.status_code == 200






    def Test_modifystory_ok(self):
        response = self.client.get('modifystory/<int:pk>/')
        assert response.status_code == 200




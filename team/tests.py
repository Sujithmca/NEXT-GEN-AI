from django.test import TestCase


class TeamPageTests(TestCase):
    def test_team_page_renders_successfully(self):
        response = self.client.get('/team/')
        self.assertEqual(response.status_code, 200)

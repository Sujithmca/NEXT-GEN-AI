from django.test import TestCase


class HomePageTests(TestCase):
    def test_homepage_is_available_at_root_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

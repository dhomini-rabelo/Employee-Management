from django.test import SimpleTestCase, Client
from django.urls import reverse


class HomePageViewTest(SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.request = cls.client.get(reverse('home'))

    def test_status(self):
        # request = self.client.get(reverse('home'))
        self.assertEqual(self.request.status_code, 200) # 200 - OK

    def test_template(self):
        # request = self.client.get(reverse('home'))
        self.assertTemplateUsed(self.request, 'pages/index.html')
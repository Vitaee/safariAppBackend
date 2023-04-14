from safari import views
from django.urls import resolve, reverse
from rest_framework.test import APISimpleTestCase

class TestSafariUrl(APISimpleTestCase):
    def test_create_safari(self):
        url = reverse('safari:create_safari')
        self.assertEqual(resolve(url).func.view_class, views.SafariCreateView)

    def test_get_all_safari(self):
        url = reverse('safari:get_all_safari')
        self.assertEqual(resolve(url).url_name, 'get_all_safari')
    
    def test_search_safari(self):
        url = reverse('safari:search_safari')
        self.assertEqual(resolve(url).func.view_class, views.SafariSearchView)
from django.urls import path
from . import views

app_name = 'safari'

urlpatterns = [
    path('create', views.SafariCreateView.as_view(), name='create'),
    path('all', views.SafariAllView.as_view({'get': 'list'}), name='get_all_safari'),
    path('filter', views.SafariSearchView.as_view(), name='search_safari')

]
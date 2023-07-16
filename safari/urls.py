from django.urls import path
from . import views

app_name = 'safari'

urlpatterns = [
    path('create', views.SafariCreateView.as_view(), name='create_safari'),
    path('all', views.SafariAllView.as_view(), name='get_all_safari'),
    path('filter', views.SafariSearchView.as_view(), name='search_safari'),
    path('rate', views.SafariRatingView.as_view({'get': 'list'}), name="safari_rating")

]
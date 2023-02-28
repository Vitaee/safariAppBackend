from django.urls import path
from . import views

app_name = 'safari'

urlpatterns = [
    path('create', views.CreateSafariView.as_view(), name='create'),
    path('all', views.GetAllSafariView.as_view(), name='get_all_safari'),

]
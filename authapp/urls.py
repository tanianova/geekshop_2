from django.urls import path

from authapp.views import LoginListView, register, logout, profile, verify

app_name = 'authapp'

urlpatterns = [
    path('login/', LoginListView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
]
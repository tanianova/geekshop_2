from django.urls import path

from mainapp.views import products

app_name = 'main'

urlpatterns = [
    path('',products,name='index'),
    path('<int:id>/',products,name='product'),
]
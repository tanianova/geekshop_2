from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp.views import products, ProductDetail

app_name = 'mainapp'

urlpatterns = [
    path('', cache_page(3600)(products), name='index'),
    path('category/<int:id>', products, name='category'),
    path('page/<int:page>/', products, name='page'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
]

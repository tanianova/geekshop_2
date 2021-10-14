from django.urls import path

from mainapp.views import products, ProductDetail

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:id>', products, name='category'),
    path('page/<int:page>/', products, name='page'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
]

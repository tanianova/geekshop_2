from django.shortcuts import render
from django.views.generic import DetailView

from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return render(request, 'mainapp/index.html')


def products(request, category_id=None, page=1):
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    paginator = Paginator(products.order_by('price'), per_page=3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context = {
        'title': 'GeekShop - Каталог',
        'products': products_paginator,
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'mainapp/products.html', context)

class ProductDetail(DetailView):
    model = Product
    template_name = 'mainapp/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, category_id=None, *args, **kwargs):
        context = super().get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context
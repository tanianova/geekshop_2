from django.shortcuts import render
from django.views.generic import DetailView

from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.cache import cache

import os
import json

from django.views.decorators.cache import cache_page, never_cache
from django.views.generic import DetailView

def get_links_category():
    if settings.LOW_CACHE:
        key = 'links_category'
        links_category = cache.get(key)

        if links_category is None:
            links_category = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_category)
        return links_category
    else:
        return ProductCategory.objects.filter(is_active=True)

def get_links_product():
    if settings.LOW_CACHE:
        key = 'links_product'
        links_product = cache.get(key)

        if links_product is None:
            links_product = Product.objects.filter(is_active=True).select_related()
            cache.set(key, links_product)
        return links_product
    else:
        return Product.objects.filter(is_active=True).select_related()

def index(request):
    return render(request, 'mainapp/index.html')

def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)

        if product is None:
            product = get_object_or_404(Product,pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product,pk=pk)

# @cache_page(3600) перенесено в url
def products(request, id=None, page=1):
    products = Product.objects.filter(category_id=id).select_related(
        'category') if id != None else Product.objects.all().select_related('category')
    # products = get_links_product()
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
        'categories': ProductCategory.objects.filter(is_active=True),
    }
    return render(request, 'mainapp/products.html', context)


class ProductDetail(DetailView):
    model = Product
    template_name = 'mainapp/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, category_id=None, *args, **kwargs):
        context = super().get_context_data()
        context['product'] = get_product(self.kwargs.get('pk'))
        context['categories'] = ProductCategory.objects.all()
        return context

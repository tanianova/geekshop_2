from django.db.models import F
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from mainapp.models import Product
from basket.models import Basket
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db import connection


@login_required
def basket_add(request, product_id):
    basket_product = get_object_or_404(Product, id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=basket_product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=basket_product, quantity=1)
        # basket = Basket(user=request.user, product=basket_product)
        # basket.quantity += 1
        # basket.save()
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        basket = baskets.first()
        # basket.quantity += 1
        baskets.quantity = F('quantity') + 1
        basket.save()

        update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
        print(f'basket_add {update_queries} ')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket = Basket.objects.get(id=int(id))
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        result = render_to_string('basket/basket.html',  request=request)
        return JsonResponse({'result': result})

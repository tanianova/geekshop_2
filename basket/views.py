from django.shortcuts import  HttpResponseRedirect,get_object_or_404
from mainapp.models import Product
from basket.models import Basket

def basket_add(request,product_id):
    basket_product = get_object_or_404(Product,id=product_id)
    baskets = Basket.objects.filter(user=request.user,product=basket_product)
    if not baskets.exists():
        basket = Basket(user=request.user, product=basket_product)
        basket.quantity +=1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        basket=baskets.first()
        basket.quantity +=1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def basket_remove(request,id):
    basket=Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




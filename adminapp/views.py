from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, BaseDetailView
from django.utils.decorators import method_decorator
from django.db import connection
from django.db.models import F

from authapp.models import User
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, ProductAdminCreateForm, ProductAdminUpdateForm, \
    CategoryUpdateFormAdmin
from mainapp.models import Product, ProductCategory


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def index(request):
    return render(request, 'adminapp/index.html')


class UserListView(ListView):
    model = User
    template_name = 'adminapp/admin-users-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users_read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('adminapp:admin_users_read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('adminapp:admin_users_read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# FBV:
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_read(request):
#     context = {
#         'users': User.objects.all()
#     }
#     return render(request, 'adminapp/admin-users-read.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admins:admin_users_read'))
#     else:
#         form = UserAdminRegisterForm()
#     context = {
#         'title': 'GeekShop - Регистрация',
#         'form': form,
#     }
#     return render(request, 'adminapp/admin-users-create.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request, id=None):
#     user = User.objects.get(id=id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:admin_users_read'))
#     else:
#         form = UserAdminProfileForm(instance=user)
#     context = {'form': form, 'current_user': user}
#     return render(request, 'adminapp/admin-users-update-delete.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_delete(request, id=None):
#     user = User.objects.get(id=id)
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect(reverse('admins:admin_users_read'))

class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/admin-products-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductListView, self).dispatch(request, *args, **kwargs)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/admin-products-create.html'
    form_class = ProductAdminCreateForm
    success_url = reverse_lazy('admins:admin_products_read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCreateView, self).dispatch(request, *args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/admin-products-update-delete.html'
    form_class = ProductAdminUpdateForm
    success_url = reverse_lazy('adminapp:admin_products_read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductUpdateView, self).dispatch(request, *args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('adminapp:admin_products_read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductDeleteView, self).dispatch(request, *args, **kwargs)


# FBV:
# def admin_products_read(request):
#     context = {'products': product.objects.all()}
#     return render(request, 'adminapp/admin-products-read.html', context)


# def admin_products_create(request):
#     if request.method == 'POST':
#         form = ProductAdminCreateForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admins:admin_products_read'))
#     else:
#         form = ProductAdminCreateForm()
#     context = {'form': form}
#     return render(request, 'adminapp/admin-products-create.html', context)


# def admin_products_update(request, id=None):
#     current_product = product.objects.get(id=id)
#     if request.method == 'POST':
#         form = ProductAdminUpdateForm(data=request.POST, files=request.FILES, instance=current_product)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:admin_products_read'))
#     else:
#         form = ProductAdminUpdateForm(instance=current_product)
#     context = {
#         'form': form,
#         'current_product': current_product
#     }
#     return render(request, 'adminapp/admin-products-update-delete.html', context)


# def admin_products_delete(request, id=None):
#     current_product = product.objects.get(id=id)
#     current_product.delete()
#     return HttpResponseRedirect(reverse('admins:admin_products_read'))

# category


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/admin-category-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryListView, self).dispatch(request, *args, **kwargs)


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admin_category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.product_set.update(is_active=False)
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryDeleteView, self).dispatch(request, *args, **kwargs)


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admin_category')
    form_class = CategoryUpdateFormAdmin

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'применяется скидка {discount} % к товарам категории {self.object.name}')
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['key'] = obj.id
        context['cat'] = obj.name
        return context

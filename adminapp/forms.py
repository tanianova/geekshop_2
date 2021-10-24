from authapp.forms import UserRegisterForm, UserProfileForm
from authapp.models import User
from django import forms
from mainapp.models import Product, ProductCategory


class UserAdminRegisterForm(UserRegisterForm):
    avatar = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'avatar')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'


class UserAdminProfileForm(UserProfileForm):
    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False

class CategoryUpdateFormAdmin(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4"}))
    # description = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4"}), required=False)
    # is_active = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-control py-4"}))
    discount = forms.IntegerField(widget=forms.NumberInput(),label='скидка',required=False,min_value=0,max_value=90,
                                  initial=0)

    class Meta:
        model = ProductCategory
        # exclude =()
        fields = ("name", "description",'discount')

    def __init__(self, *args, **kwargs):
        super(CategoryUpdateFormAdmin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class ProductAdminCreateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = Product
        fields = ('name', 'category', 'quantity', 'price', 'short_description', 'description', 'image')

    def __init__(self, *args, **kwargs):
        super(ProductAdminCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите наименование продукта'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Введите количество'
        self.fields['price'].widget.attrs['placeholder'] = 'Введите цену'
        self.fields['short_description'].widget.attrs['placeholder'] = 'Короткое описание продукта'
        self.fields['description'].widget.attrs['placeholder'] = 'Полное описание продукта'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class ProductAdminUpdateForm(ProductAdminCreateForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'quantity', 'price', 'short_description', 'description', 'image')
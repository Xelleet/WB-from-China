from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, AdminForm, LoginForm, DeleteProductForm, RegisterForm
from .models import Product, Admin, CartProduct
from django.contrib.auth import authenticate, logout, login

@login_required()
def index(request):
    return render(request, 'index.html', {'products': Product.objects.all()})

@login_required()
def cart(request):
    cart_products = CartProduct.objects.filter(user=request.user)
    product_ids = [item.product_id for item in cart_products] #скажу честно, стырил у chatgpt :(
    products = Product.objects.filter(id__in=product_ids)
    cart_product_map = {item.product_id: item for item in cart_products}
    return render(request, 'cart.html', {'products': products, 'cart_product_map': cart_product_map, 'user': request.user})

def add_to_cart(request, index):
    if not request.user.is_authenticated:
        return redirect('login_user')

    product = get_object_or_404(Product, id=index)

    # Add the product to the cart for the logged-in user
    cart_product = CartProduct(user=request.user, product=product)
    cart_product.save()

    return redirect('index')

def remove_from_cart(request, index):
    product = get_object_or_404(CartProduct, product=Product.objects.get(id=index))
    product.delete()
    return redirect('index')

def product(request, index):
    return render(request, 'product.html', {'product': Product.objects.get(id=index)})

def delete_product(request): #Это конечно чистой воды колхоз, но я хз как это делается на том же wb, так что пофиг
    if request.method == 'POST':
        form = DeleteProductForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            product = get_object_or_404(Product, id=id)
            product.delete()
            return redirect('index')
    else:
        form = DeleteProductForm()
    return render(request, 'delete_product.html', {'form':form, 'products': Product.objects.all()})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            login(request, user)  # Log in the new user
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def add_admin(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.save()
            return redirect('index')
    else:
        form = AdminForm()
    return render(request, 'add_admin.html', {'form': form})

def wb_admin(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('index')
    else:
        form = ProductForm()
    return render(request, 'wb_admin.html', {'form': form})
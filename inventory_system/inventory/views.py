from django.shortcuts import render,redirect
from .forms import CategoryForm,ProductForm
from .models import Category,Product
# Create your views here.

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request,'add_category.html',{'form':form})
    
def category_list(request):
    categories = Category.objects.filter(is_active=True)
    return render(request,'category_list.html',{'categories':categories})

def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request,'product_list.html',{'products':products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('product_list')
    else:
        form = ProductForm()
    return render(request,'add_product.html',{'form':form})

def update_product(request,id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request,'update_product.html',{'form':form})

def delete_product(request,id):
    product = Product.objects.get(id=id)
    product.is_active = False
    product.status = 'out_of_stock'
    product.save()
    return redirect('product_list')

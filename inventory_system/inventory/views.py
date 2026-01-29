from django.shortcuts import render,redirect
from .forms import CategoryForm,ProductForm,StockForm
from .models import Category,Product,StockLog
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

def stock_in(request,id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity']
            product.quantity += qty
            product.status = 'available'
            product.save()
            StockLog.objects.create(product=product,change_type='in',quantity=qty)
            return redirect('product_list')
    else:
        form = StockForm()
    return render(request,'stock_in.html',{'form':form,'product':product})

def stock_out(request,id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity']
            if qty>product.quantity:
                form.add_error('quantity','Not Enough Stock Available')
            else:    
                product.quantity -=qty
                if product.quantity == 0:
                    product.status = 'out_of_stock'
                product.save()
                StockLog.objects.create(product=product,quantity=qty,change_type='out')
                return redirect('product_list')
    else:
        form = StockForm()
    return render(request,'stock_out.html',{'form':form,'product':product})
from django.shortcuts import render, redirect, get_object_or_404
from .models import *


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    ctx = {'products': products, 'categories': categories}
    return render(request, 'index.html', ctx)

def create_brand(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        if name and description and image:
            Brand.objects.create(
                name=name,
                description=description,
                image=image,
            )
            return redirect('home')
    return render(request, 'products/brand-create.html')

def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            Category.objects.create(
                name=name,
                description=description,
            )
            return redirect('home')
    return render(request, 'products/category-create.html')

def create_color(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        hex_code = request.POST.get('hex_code')
        if name and hex_code:
            Color.objects.create(
                name=name,
                hex_code=hex_code,
            )
            return redirect('home')
    return render(request, 'products/color-create.html')

def product_list(request):
    products = Product.objects.all()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    brand = request.GET.get('brand')
    color = request.GET.get('color')
    sort = request.GET.get('sort')

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if brand:
        products = products.filter(brand=brand)
    if color:
        products = products.filter(color=color)
    if sort == 'low_to_high':
        products = products.order_by('price')
    elif sort == 'high_to_low':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')

    brands = Brand.objects.all()
    categories = Category.objects.all()
    colors = Color.objects.all()

    ctx = {
        'products': products,
        'brands': brands,
        'categories': categories,
        'colors': colors
    }
    return render(request, 'products/product-by-category.html', ctx)

def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category')
        color_id = request.POST.get('color')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        if name and price and brand_id and category_id and color_id and description and image:
            brand = Brand.objects.get(id=brand_id)
            category = Category.objects.get(id=category_id)
            color = Color.objects.get(id=color_id)

            Product.objects.create(
                name=name,
                price=price,
                brand=brand,
                category=category,
                color=color,
                description=description,
                image=image,
            )
            return redirect('products:list')
    brands = Brand.objects.all()
    categories = Category.objects.all()
    colors = Color.objects.all()
    ctx = {
        'brands': brands,
        'categories': categories,
        'colors': colors,
    }
    return render(request, 'products/product-create.html', ctx)

def product_detail(request, year, month, day, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        created_at__year=year,
        created_at__month=month,
        created_at__day=day
    )
    reviews = Review.objects.filter(product=product)
    ctx = {'product': product,
           'reviews': reviews,}
    return render(request, 'products/product-detail.html', ctx)


def create_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        if name and review:
            Review.objects.create(
                name=name,
                rating=rating,
                review=review,
                product=product
            )
            return redirect(product.get_success_commented_url())
    reviews = Review.objects.filter(product=product)
    ctx = {
        'product': product,
        'reviews': reviews,
    }
    return render(request, 'products/product-detail.html', ctx)

def success_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/success-commented.html', {'product': product})

from django.shortcuts import render, redirect
from .models import Food, Review, Category
from .forms import ReviewForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    popular_dishes = Food.objects.filter(is_popular=True)
    reviews = Review.objects.order_by('-created_at')
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReviewForm()

    return render(request, 'restaurant/home.html', {
        'popular_dishes': popular_dishes,
        'reviews': reviews,
        'form': form,
        'categories': categories
    })
@require_POST
def add_review(request):
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save()
        return JsonResponse({
            'success': True,
            'name': review.name,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.strftime('%d %b %Y')
        })
    return JsonResponse({'success': False, 'errors': form.errors})

def custom_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=identifier, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # home page
        else:
            messages.error(request, 'Invalid credentials')

    return redirect('/')

def custom_logout(request):
    logout(request)
    return redirect('/')

def register_user(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # email or phone
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('/')

        if User.objects.filter(username=identifier).exists():
            messages.error(request, 'Account already exists')
            return redirect('/')

        User.objects.create_user(
            username=identifier,   # email OR phone
            password=password
        )

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('/')

    return render(request, 'restaurant/register.html')

def menu_page(request):
    foods = Food.objects.all()
    categories = Category.objects.all()
    return render(request, 'restaurant/menu.html', {
        'foods': foods,
        'categories': categories
    })

def foods_by_category(request, category_id):
    foods = Food.objects.filter(category_id=category_id)

    data = []
    for food in foods:
        data.append({
            'id': food.id,
            'name': food.name,
            'price': str(food.price),
            'image': food.image.url,
        })

    return JsonResponse({'foods': data})

@require_POST
def add_to_cart(request):
    food_id = str(request.POST.get('food_id'))

    cart = request.session.get('cart', {})

    if food_id in cart:
        cart[food_id]['quantity'] += 1
    else:
        food = Food.objects.get(id=food_id)
        cart[food_id] = {
            'name': food.name,
            'price': str(food.price),
            'quantity': 1,
            'image': food.image.url
        }

    request.session['cart'] = cart
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'cart_count': sum(item['quantity'] for item in cart.values())
    })
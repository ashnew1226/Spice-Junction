from django.shortcuts import render, redirect, get_object_or_404
from .models import Food, Review, Category, Cart, CartItem
from .forms import ReviewForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    popular_dishes = Food.objects.filter(is_popular=True)
    reviews = Review.objects.order_by('-created_at')
    categories = Category.objects.all()
    cart_count = 0
    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        cart_count = sum(item.quantity for item in cart.items.all())   
        name = request.user.username.split("@")[0]
    else:
        cart = None
        cart_count = 0
        name = None
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
        'categories': categories,
        'cart_count':cart_count,
        'name':name
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
    return render(request, 'restaurant/menu.html', {'categories': categories})

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

def get_user_cart(user):
    print(f"user - {user}")
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

# @login_required
from django.http import JsonResponse

def ajax_add_to_cart(request):

    # 🔥 MUST be first
    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "error": "login_required"
        }, status=401)

    if request.method == "POST":

        food_id = request.POST.get("food_id")

        food = get_object_or_404(Food, id=food_id)
        cart = get_user_cart(request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            food=food
        )

        if not created:
            cart_item.quantity += 1
        cart_item.save()

        cart_count = sum(item.quantity for item in cart.items.all())

        return JsonResponse({
            "success": True,
            "food_id": food.id,
            "quantity": cart_item.quantity,
            "cart_count": cart_count
        })

    return JsonResponse({
        "success": False
    })

@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()
    items = cart.items.all() if cart else []
    name = request.user.username.split("@")[0]
    return render(request, 'restaurant/cart_detail.html', {
        'cart': cart,
        'items': items,
        'name':name
    })
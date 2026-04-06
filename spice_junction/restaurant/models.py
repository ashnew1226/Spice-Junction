from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)  # Veg / Non-Veg / Drinks
    def __str__(self):
        return self.name

class Food(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='foods/')
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,on_delete=models.CASCADE,
        related_name='items'
    )
    food = models.ForeignKey(
        'Food',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'food'], name='unique_cart_food')
        ]
    def __str__(self):
        return f"{self.food.name} ({self.quantity})"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}⭐"

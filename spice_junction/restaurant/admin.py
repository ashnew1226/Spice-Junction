from django.contrib import admin

# Register your models here.
from .models import Category, Food, Review

admin.site.register(Category)
admin.site.register(Food)
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'created_at')
    list_filter = ('rating',)
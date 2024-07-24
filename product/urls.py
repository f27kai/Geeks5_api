from django.urls import path
from .views import (
    products_list_api_view,
    products_detail_api_view,
    reviews_list_api_view,
    reviews_detail_api_view,
    categories_list_api_view,
    categories_detail_api_view
)

urlpatterns = [
    path('categories/', categories_list_api_view, name='category-list'),
    path('categories/<int:id>/', categories_detail_api_view, name='category-detail'),
    path('products/', products_list_api_view, name='product-list'),
    path('products/<int:id>/', products_detail_api_view, name='product-detail'),
    path('reviews/', reviews_list_api_view, name='review-list'),
    path('reviews/<int:id>/', reviews_detail_api_view, name='review-detail'),
]

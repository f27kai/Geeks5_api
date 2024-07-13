from django.urls import path
from .views import (
    category_list_api_view,
    category_detail_api_view,
    product_list_api_view,
    product_detail_api_view,
    review_list_api_view,
    review_detail_api_view,
    product_reviews_list_api_view
)

urlpatterns = [
    path('categories/', category_list_api_view, name='category-list'),
    path('categories/<int:id>/', category_detail_api_view, name='category-detail'),
    path('products/', product_list_api_view, name='product-list'),
    path('products/<int:id>/', product_detail_api_view, name='product-detail'),
    path('products/reviews/', product_reviews_list_api_view, name='product-reviews-list'),
    path('reviews/', review_list_api_view, name='review-list'),
    path('reviews/<int:id>/', review_detail_api_view, name='review-detail'),
]

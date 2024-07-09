from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from .models import Category, Product, Review

@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()
    data = CategorySerializer(categories, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"error_message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    data = CategorySerializer(category).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data = ProductSerializer(products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"error_message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    data = ProductSerializer(product).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(reviews, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({"error_message": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(review).data
    return Response(data=data, status=status.HTTP_200_OK)


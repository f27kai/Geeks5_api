from django.db.models import Avg, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductWithReviewsSerializer
from .models import Category, Product, Review
from rest_framework.generics import get_object_or_404



@api_view(['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.annotate(products_count=Count('product'))
        data = CategorySerializer(categories, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_update_delete_api_view(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'GET':
        data = CategorySerializer(category).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_update_delete_api_view(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'GET':
        data = ProductSerializer(product).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_update_delete_api_view(request, id):
    review = get_object_or_404(Review, id=id)

    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def product_reviews_list_api_view(request):
    products = Product.objects.annotate(rating=Avg('review__stars')).prefetch_related('review_set')
    data = ProductWithReviewsSerializer(products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)




# @api_view(['GET'])
# def product_reviews_list_api_view(request):
#     products = Product.objects.annotate(rating=Avg('review__stars')).prefetch_related('review_set')
#     data = ProductWithReviewsSerializer(products, many=True).data
#     return Response(data=data, status=status.HTTP_200_OK)
#
# @api_view(['GET'])
# def category_list_api_view(request):
#     categories = Category.objects.all()
#     data = CategorySerializer(categories, many=True).data
#     return Response(data=data, status=status.HTTP_200_OK)
#
# @api_view(['GET'])
# def category_detail_api_view(request, id):
#     try:
#         category = Category.objects.get(id=id)
#     except Category.DoesNotExist:
#         return Response({"error_message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
#     data = CategorySerializer(category).data
#     return Response(data=data, status=status.HTTP_200_OK)
#
# @api_view(['GET'])
# def product_list_api_view(request):
#     products = Product.objects.all()
#     data = ProductSerializer(products, many=True).data
#     return Response(data=data, status=status.HTTP_200_OK)
#
# @api_view(['GET'])
# def product_detail_api_view(request, id):
#     try:
#         product = Product.objects.get(id=id)
#     except Product.DoesNotExist:
#         return Response({"error_message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
#     data = ProductSerializer(product).data
#     return Response(data=data, status=status.HTTP_200_OK)
#
# @api_view(['GET'])
# def review_list_api_view(request):
#     reviews = Review.objects.all()
#     data = ReviewSerializer(reviews, many=True).data
#     return Response(data=data, status=status.HTTP_200_OK)
#
# @api_view(['GET'])
# def review_detail_api_view(request, id):
#     try:
#         review = Review.objects.get(id=id)
#     except Review.DoesNotExist:
#         return Response({"error_message": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
#     data = ReviewSerializer(review).data
#     return Response(data=data, status=status.HTTP_200_OK)


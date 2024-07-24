from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, CategoryValueSerializer, ReviewSerializer, ReviewValidateSerializer, ProductSerializer, ProductValidateSerializer
from .models import Category, Product, Review, Tag
from rest_framework.generics import get_object_or_404

@api_view(['GET', 'POST'])
def products_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        title = serializer.validated_data['title']
        description = serializer.validated_data.get('description', '')
        price = serializer.validated_data['price']
        category_id = serializer.validated_data['category']
        tags = serializer.validated_data.get('tags', [])

        if not Category.objects.filter(id=category_id).exists():
            return Response(data={'error': 'Category does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        existing_tags = Tag.objects.filter(id__in=tags).values_list('id', flat=True)
        missing_tags = set(tags) - set(existing_tags)
        if missing_tags:
            return Response(data={'error': f'Tags with ids {list(missing_tags)} do not exist'},
                            status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.create(title=title, description=description, price=price, category_id=category_id)
        product.tags.set(tags)
        product.save()

        return Response(data=ProductSerializer(product).data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def products_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ProductSerializer(product).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(product, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        title = serializer.validated_data.get('title', product.title)
        description = serializer.validated_data.get('description', product.description)
        price = serializer.validated_data.get('price', product.price)
        category_id = serializer.validated_data.get('category', product.category_id)
        tags = serializer.validated_data.get('tags', product.tags.values_list('id', flat=True))

        if not Category.objects.filter(id=category_id).exists():
            return Response(data={'error': 'Category does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        existing_tags = Tag.objects.filter(id__in=tags).values_list('id', flat=True)
        missing_tags = set(tags) - set(existing_tags)
        if missing_tags:
            return Response(data={'error': f'Tags with ids {list(missing_tags)} do not exist'},
                            status=status.HTTP_400_BAD_REQUEST)

        product.title = title
        product.description = description
        product.price = price
        product.category_id = category_id
        product.tags.set(tags)
        product.save()

        return Response(data=ProductSerializer(product).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        product.delete()
        return Response(data={'product_id': id}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def reviews_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data['text']
        product_id = serializer.validated_data['product']
        stars = serializer.validated_data['stars']

        if not Product.objects.filter(id=product_id).exists():
            return Response(data={'error': 'Product does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        review = Review.objects.create(product_id=product_id, stars=stars, text=text)
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def reviews_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(review, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data.get('text', review.text)
        product_id = serializer.validated_data.get('product', review.product_id)
        stars = serializer.validated_data.get('stars', review.stars)

        if not Product.objects.filter(id=product_id).exists():
            return Response(data={'error': 'Product does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        review.text = text
        review.product_id = product_id
        review.stars = stars
        review.save()

        return Response(data=ReviewSerializer(review).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        review.delete()
        return Response(data={'review_id': id}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def categories_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name = serializer.validated_data['name']
        category = Category.objects.create(name=name)
        return Response(data=CategorySerializer(category).data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def categories_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = CategorySerializer(category).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        category.name = serializer.validated_data.get('name', category.name)
        category.save()
        return Response(data=CategorySerializer(category).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        category.delete()
        return Response(data={'category_id': id}, status=status.HTTP_204_NO_CONTENT)

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


from django.db.models import Avg
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Category, Product, Review, Tag

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, category):
        return category.product_set.count()

class CategoryValueSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=50)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'text', 'stars']

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=1, max_length=100)
    product = serializers.IntegerField(min_value=1)
    stars = serializers.IntegerField(min_value=1, max_value=5)

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'average_rating']

    def get_average_rating(self, product):
        reviews = product.reviews.all()
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('stars'))['stars__avg']
            return average_rating
        return None

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=50)
    description = serializers.CharField(min_length=1, max_length=100, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    category = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1), required=False)

    def validate_tags(self, tags):
        tag_a = set(tags)
        tag_db = Tag.objects.filter(id__in=tag_a)
        if len(tag_db) != len(tag_a):
            raise ValidationError("Some tags do not exist.")

        return tags



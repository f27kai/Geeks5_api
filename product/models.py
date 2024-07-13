from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Review for {self.product.title} with {self.stars} stars"


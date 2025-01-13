from django.utils.text import slugify
from django.urls import reverse
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='brands/')

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'

class Color(models.Model):
    name = models.CharField(max_length=200)
    hex_code = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_detail_url(self):
        return reverse('products:detail', args=[
            self.created_at.year,
            self.created_at.month,
            self.created_at.day,
            self.slug
        ])

    def get_success_commented_url(self):
        return reverse('products:success_review', args=[self.pk])

    def __str__(self):
        return f'{self.name}'

class Review(models.Model):
    name = models.CharField(max_length=200)
    rating = models.CharField(max_length=200, null=True)
    review = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"{self.name} - {self.rating} Stars"


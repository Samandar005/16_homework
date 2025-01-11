from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('list/', views.product_list, name='list'),
    path('create/brand/', views.create_brand, name='brand_create'),
    path('create/category/', views.create_category, name='category_create'),
    path('create/color/', views.create_color, name='create_color'),
    path('create/product', views.create_product, name='product_create'),
    path('create/review/<int:pk>/', views.create_review, name='reviews_create'),
    path('success/review/<int:pk>/', views.success_review, name='success_review'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.product_detail, name='detail'),
]

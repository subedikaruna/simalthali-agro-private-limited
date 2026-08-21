from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("goats/", views.goat_list, name="goat_list"),
    path("goats/<int:pk>/", views.goat_detail, name="goat_detail"),
    path("products/", views.product_list, name="product_list"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("contact/", views.contact, name="contact"),
]

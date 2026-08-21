from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import AboutPage, Goat, Product, BlogPost
from .forms import ContactForm


def home(request):
    featured_goats = Goat.objects.filter(is_featured=True)[:4]
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    return render(request, "core/home.html", {
        "featured_goats": featured_goats,
        "latest_posts": latest_posts,
    })


def about(request):
    about_page = AboutPage.load()
    return render(request, "core/about.html", {"about": about_page})


def goat_list(request):
    goats = Goat.objects.select_related("breed").all()
    return render(request, "core/goats.html", {"goats": goats})


def goat_detail(request, pk):
    goat = get_object_or_404(Goat, pk=pk)
    return render(request, "core/goat_detail.html", {"goat": goat})


def product_list(request):
    products = Product.objects.filter(is_available=True)
    return render(request, "core/products.html", {"products": products})


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, "core/blog_list.html", {"posts": posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, "core/blog_detail.html", {"post": post})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your message has been sent — we'll get back to you soon.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})

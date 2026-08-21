from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect
from .models import AboutPage, Breed, Goat, Product, BlogPost, ContactMessage


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    """
    Singleton admin: there's only ever one About Page row.
    Clicking "About Page" in the sidebar jumps straight to editing it
    instead of showing a list.
    """

    list_display = ("title", "updated_at")

    def has_add_permission(self, request):
        # Block adding a second row once one exists
        return not AboutPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        about = AboutPage.load()
        return redirect(reverse("admin:core_aboutpage_change", args=[about.pk]))


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Goat)
class GoatAdmin(admin.ModelAdmin):
    list_display = ("name", "ear_tag_number", "breed", "sex", "date_of_birth", "mother", "father", "is_available_for_sale", "is_featured")
    list_filter = ("breed", "sex", "is_available_for_sale", "is_featured")
    search_fields = ("name", "ear_tag_number")  # required for autocomplete_fields to work (incl. self-referencing mother/father)
    autocomplete_fields = ("mother", "father")
    list_editable = ("is_available_for_sale", "is_featured")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "unit", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name",)
    list_editable = ("is_available",)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at", "is_read")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "phone", "message", "created_at")
    list_editable = ("is_read",)


# Customize the admin panel header/title
admin.site.site_header = "Goat Farm Admin"
admin.site.site_title = "Goat Farm Admin"
admin.site.index_title = "Manage your farm website"
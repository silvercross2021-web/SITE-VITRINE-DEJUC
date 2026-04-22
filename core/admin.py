"""
Admin configuration for DEJUC INTERNATIONAL GROUP
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Service, ServiceFeature, ServiceStep, ServiceFAQ,
    TeamMember, Testimonial, BlogPost,
    ContactMessage, NewsletterSubscriber, LatinMaxim
)


# ─── Inlines ──────────────────────────────────────────────────────────────────

class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 3
    fields = ['feature', 'order']


class ServiceStepInline(admin.TabularInline):
    model = ServiceStep
    extra = 2
    fields = ['step_number', 'title', 'description']


class ServiceFAQInline(admin.TabularInline):
    model = ServiceFAQ
    extra = 2
    fields = ['question', 'answer', 'order']


# ─── Model Admins ─────────────────────────────────────────────────────────────

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['number', 'title', 'color_class', 'is_featured', 'order']
    list_editable = ['is_featured', 'order']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceFeatureInline, ServiceStepInline, ServiceFAQInline]
    search_fields = ['title', 'short_description']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('features', 'steps', 'faqs')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'title', 'role', 'is_featured', 'order']
    list_editable = ['is_featured', 'order']
    search_fields = ['full_name', 'title']
    list_filter = ['role', 'is_featured']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'company', 'rating_stars', 'is_featured', 'created_at']
    list_editable = ['is_featured']
    list_filter = ['rating', 'is_featured']
    search_fields = ['client_name', 'company', 'content']

    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html('<span title="{}/5">{}</span>', obj.rating, stars)
    rating_stars.short_description = 'Note'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'is_featured', 'views', 'published_at']
    list_editable = ['is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['category', 'is_published', 'is_featured']
    search_fields = ['title', 'excerpt', 'content']
    date_hierarchy = 'published_at'
    readonly_fields = ['views', 'created_at', 'updated_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'service', 'status', 'created_at']
    list_filter = ['status', 'service', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    readonly_fields = ['ip_address', 'created_at', 'updated_at']
    list_editable = ['status']
    date_hierarchy = 'created_at'

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Nom complet'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Mark new messages with visual indicator
        return qs

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['new_count'] = ContactMessage.objects.filter(status='new').count()
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active']
    search_fields = ['email']
    list_editable = ['is_active']


@admin.register(LatinMaxim)
class LatinMaximAdmin(admin.ModelAdmin):
    list_display = ['latin_text', 'french_translation', 'order', 'is_active']
    list_editable = ['order', 'is_active']

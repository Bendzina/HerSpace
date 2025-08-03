from django.contrib import admin
from .models import WisdomMessage, UserWisdomDelivery, UserProfile, RitualUsage

@admin.register(WisdomMessage)
class WisdomMessageAdmin(admin.ModelAdmin):
    list_display = ("title", "for_mood_context", "for_support_style", "is_active", "created_at")
    search_fields = ("title", "message", "affirmation")
    list_filter = ("for_mood_context", "for_support_style", "is_active")

@admin.register(UserWisdomDelivery)
class UserWisdomDeliveryAdmin(admin.ModelAdmin):
    list_display = ("user", "wisdom_message", "delivered_at", "was_helpful")
    list_filter = ("was_helpful",)
    search_fields = ("user__username", "wisdom_message__title")

@admin.register(RitualUsage)
class RitualUsageAdmin(admin.ModelAdmin):
    list_display = ("user", "ritual", "used_at", "was_helpful", "effectiveness_rating")
    list_filter = ("was_helpful", "effectiveness_rating", "mood_before", "mood_after")
    search_fields = ("user__username", "ritual__title", "notes")
    readonly_fields = ("used_at",)

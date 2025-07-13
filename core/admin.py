from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Club

# Register your models here.

# admin.site.register(User, UserAdmin)

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'city', 'foundation_year', 'titles_won', 'coach_name', 'image')
    list_editable = ('description', 'city', 'foundation_year', 'titles_won', 'coach_name', 'image')
    list_display_links = ('name',)
    search_fields = ('name', 'city', 'coach_name')
    list_filter = ('city', 'foundation_year')
    ordering = ('name',)
    list_per_page = 10
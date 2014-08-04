from django.contrib import admin

from core.models import FeaturedMedia

class FeaturedMediaAdmin(admin.ModelAdmin):
    list_display = ('header','description')

admin.site.register(FeaturedMedia, FeaturedMediaAdmin)

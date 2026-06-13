from django.contrib import admin
from django.utils.html import format_html
from .models import Realty, RealtyPhoto, Favorite


class RealtyPhotoInline(admin.TabularInline):
    model = RealtyPhoto
    extra = 1
    max_num = 10
    fields = ('image', 'order', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;">', obj.image.url)
        return '—'
    preview.short_description = 'Превью'


@admin.register(Realty)
class RealtyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'realty_type', 'price', 'area', 'floors', 'created_at')
    list_filter = ('realty_type', 'floors')
    search_fields = ('title', 'address', 'owner__email')
    inlines = [RealtyPhotoInline]
    raw_id_fields = ('owner',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'realty', 'added_at')
    search_fields = ('user__email', 'realty__title')

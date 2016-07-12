from django.contrib import admin

from feincms_simplegallery.util.base import (
    BaseElement,
    BaseContainer,
    )
from feincms_simplegallery.models import (
    GalleryContainer,
    GalleryElement,
    GalleryContent,
    )


class BaseElementAdmin(admin.TabularInline):
    extra = 0
    sortable_field_name = "_order"


class BaseContainerAdmin(admin.ModelAdmin):
    list_display = ('title',)
    save_as = True


class GalleryElementAdmin(BaseElementAdmin):
    model = GalleryElement
    raw_id_fields = ('mediafile', 'page')


@admin.register(GalleryContainer)
class GalleryContainerAdmin(BaseContainerAdmin):
    inlines = [GalleryElementAdmin]
    list_editable = (
        # 'title',
        '_order',
        )
    list_display = (
        'title',
        '_order',
        )
    ordering = (
        '_order',
        'title',
        ) 

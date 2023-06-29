from django.contrib import admin

from .models import *

class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'picture', 'time_create', 'printed')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'picture')


class CategoryInline(admin.TabularInline):
    model = Classifing
    raw_id_fields = ('classes', 'category')

@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    list_display_links = ('name', )
    search_fields = ('name',)
    inlines = [CategoryInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name', )

@admin.register(ClientWordForm)
class ClientWordFormAdmin(admin.ModelAdmin):
    raw_id_fields = ('client', 'wordform')


admin.site.register(Root)
admin.site.register(Binyan)
admin.site.register(Grouping)
admin.site.register(Word, WordAdmin)
admin.site.register(WordForm)
admin.site.register(Expression)


from django.contrib import admin

from .models import *

class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'picture', 'time_create', 'printed')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'picture')

admin.site.register(Root)
admin.site.register(Binyan)
admin.site.register(Classes)
admin.site.register(Category)
admin.site.register(Classifing)
admin.site.register(Grouping)
admin.site.register(Word, WordAdmin)
admin.site.register(WordForm)
admin.site.register(Expression)

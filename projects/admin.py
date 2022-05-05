from django.contrib import admin
from .models import Project, Category, Tag, Rate

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Rate)

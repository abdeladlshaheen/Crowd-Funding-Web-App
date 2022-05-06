from django.contrib import admin
from .models import Comment, Picture, Project, Category, ProjectDonation, Tag, UserRateProject

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ProjectDonation)
admin.site.register(UserRateProject)
admin.site.register(Picture)
admin.site.register(Comment)


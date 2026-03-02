from django.contrib import admin
from .models import (
    Profile, Skill, Project, ProjectImage,
    Experience, Education, Certification,
    ContactMessage
)

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "summary", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "location")

admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Certification)
admin.site.register(ContactMessage)
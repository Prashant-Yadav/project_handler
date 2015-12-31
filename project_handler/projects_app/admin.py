from django.contrib import admin

from .models import User, Student, Mentor, Project, Batch, Course, ProjectDocument


# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Mentor)
admin.site.register(Project)
admin.site.register(Batch)
admin.site.register(Course)
admin.site.register(ProjectDocument)
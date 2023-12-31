from django.contrib import admin
from .models import Lecture,Course,Instructor,Batch

# Register your models here.

admin.site.register(Lecture)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Batch)
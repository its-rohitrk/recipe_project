from django.contrib import admin
from .models import Department, StudentId, Student, Receipe, Subject, SubjectMarks

class SubjectMarksAdmin(admin.ModelAdmin):
    list_display = ["student", "subject", "marks"]

# Register the models
admin.site.register(Department)
admin.site.register(StudentId)
admin.site.register(Student)
admin.site.register(Receipe)
admin.site.register(Subject)
admin.site.register(SubjectMarks, SubjectMarksAdmin)

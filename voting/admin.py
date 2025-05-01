from django.contrib import admin

# Register your models here.
from .models import Session, Question, Vote, Department
admin.site.register(Session)
admin.site.register(Question)
admin.site.register(Vote)
admin.site.register(Department)

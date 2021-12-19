from django.contrib import admin

from .models import Job, Candidate, Skill

admin.site.register(Skill)
admin.site.register(Candidate)
admin.site.register(Job)

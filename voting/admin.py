from django.contrib import admin
from .models import VotingSession, Question, Vote

class VotingSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    filter_horizontal = ('users', 'submitted_by')  # Makes it easier to assign users

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text',)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'question', 'choice')
    list_filter = ('session', 'choice')

admin.site.register(VotingSession, VotingSessionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote, VoteAdmin)

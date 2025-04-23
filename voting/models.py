from django.db import models
from django.contrib.auth.models import User




# Health Cards, chose to call the model 'Question' as is's shorter
class Question(models.Model):
    question_content = models.TextField() # the actual question displayed in the heading of the card
    # hints to be displayed when user hovers on either red or green
    question_hint_red = models.TextField()
    question_hint_green = models.TextField()

    def __str__(self):
        return f"{self.question_content} - Question ID: {self.pk}"
    
# Model for the voting session
# Questions (health cards in the ERD) which will contain a question to be linked to session 
class Session(models.Model):
    title = models.CharField(max_length=255, blank=True, default='') # (optional) user can give each session a title to make them easier to distinguish in the admin view
    created_at = models.DateTimeField(auto_now=True, editable=True)
    users = models.ManyToManyField(User, related_name="voting_sessions") # which users were assigned the session [MIGHT DELETE THAT LATER]
    questions_included = models.ManyToManyField(Question, related_name="voting_sessions")
    submitted_by = models.ManyToManyField(User, related_name="submitted_sessions", blank=True) # will store users who submitted the session already

    def __str__(self):
        return f"{self.title} - Session ID: {self.pk} - {self.created_at}"
    
    def is_completed_by_user(self, user):
        # will check if a given user has already completed the session
        # will either retirn True or False
        return self.submitted_by.filter(id=user.id).exists()

#will store the user's response to a question
class Vote(models.Model):
    vote_options = ["green", "amber", "red"]

    user = models.ForeignKey(User, on_delete=models.CASCADE) # which user voted
    session = models.ForeignKey(Session, on_delete=models.CASCADE) # in which session was that
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # what was the question
    choice = models.CharField(max_length=5) # did the user answer the question
    comment = models.TextField(blank=True, null=True) # optional comment the user can add, field not required

    class Meta:
        unique_together = ('user', 'session', 'question') # idk if that's still needed 

    def __str__(self):
        return f"Vote ID:{self.pk} - {self.user.username} - {self.session.title} - {self.question.question_content}"

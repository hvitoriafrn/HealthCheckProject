from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



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

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="voting_sessions") # which users were assigned the session [MIGHT DELETE THAT LATER]
    questions_included = models.ManyToManyField(Question, related_name="voting_sessions")
    submitted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="submitted_sessions", blank=True) # will store users who submitted the session already

    def __str__(self):
        return f"{self.title} - Session ID: {self.pk} - {self.created_at}"
    
    def is_completed_by_user(self, user):
        # will check if a given user has already completed the session
        # will either retirn True or False

        return self.submitted_by.filter(userID=user.userID).exists()

#will store the user's response to a question
class Vote(models.Model):
    vote_options = ["green", "amber", "red"]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # which user voted
    session = models.ForeignKey(Session, on_delete=models.CASCADE) # in which session was that
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # what was the question
    choice = models.CharField(max_length=5) # how did the user answer the question
    comment = models.TextField(blank=True, null=True) # optional comment the user can add, field not required

    class Meta:
        unique_together = ('user', 'session', 'question') # idk if that's still needed, I kept it to be safe 

    def __str__(self):

        return f"Vote ID:{self.pk} - {self.user.email} - {self.session.title} - {self.question.question_content}"

#creating  team model
class Team(models.Model):
    teamID = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=100)
    teamCapacity = models.IntegerField(default=10)

    def __str__(self):
        return self.teamName

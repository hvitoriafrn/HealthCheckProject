from django.db import models
from django.contrib.auth.models import User

class VotingSession(models.Model):
    """A voting session for tracking satisfaction at a given time."""
    title = models.CharField(max_length=255)  # Name of the session
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    users = models.ManyToManyField(User, related_name="voting_sessions")  # Assigned users
    submitted_by = models.ManyToManyField(User, related_name="submitted_sessions", blank=True)  # Users who submitted

    def is_completed_by_user(self, user):
        """Check if a user has submitted their votes."""
        return self.submitted_by.filter(id=user.id).exists()

    def __str__(self):
        return self.title

class Question(models.Model):
    """A standard question used in voting sessions."""
    text = models.TextField()

    def __str__(self):
        return self.text

class Vote(models.Model):
    """Stores the user's response to a question in a session."""
    VOTE_CHOICES = [
        ('green', 'Happy'),
        ('amber', 'Unsure'),
        ('red', 'Unhappy'),
    ]

    #relationship with other tables defined here 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(VotingSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    choice = models.CharField(max_length=10, choices=VOTE_CHOICES) #TBC
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'session', 'question')  # Prevent duplicate votes

    def __str__(self):
        return f"{self.user.username} - {self.session.title} - {self.question.text[:50]}"

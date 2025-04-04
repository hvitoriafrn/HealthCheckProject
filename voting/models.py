from django.db import models
#from django.contrib.auth.models import User

VOTE_CHOICES = (
    ('green', 'Happy'),
    ('amber', 'Not Sure'),
    ('red', 'Unhappy'),
)

class VotingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="voting_sessions")
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Session {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class QuestionTemplate(models.Model):
    number = models.PositiveIntegerField()
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"Q{self.number}: {self.text}"

class Vote(models.Model):
    voting_session = models.ForeignKey(VotingSession, on_delete=models.CASCADE, related_name="votes")
    question_template = models.ForeignKey(QuestionTemplate, on_delete=models.CASCADE)
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES)
    comment = models.TextField(blank=True, null=True)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voting_session', 'question_template')

    def __str__(self):
        return f"Session {self.voting_session.id} - Q{self.question_template.number}: {self.vote}"

from django import forms
from .models import Vote, VOTE_CHOICES

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['vote', 'comment']
        widgets = {
            'vote': forms.RadioSelect(choices=VOTE_CHOICES),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional comments...'}),
        }

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['vote', 'comment']
        widgets = {
            'vote': forms.RadioSelect(choices=VOTE_CHOICES, attrs={'class': 'radio-input'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional comments...'}),
        }
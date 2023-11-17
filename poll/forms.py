from django import forms
from api.models import Poll,Vote

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['book']

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'books']
        widgets = {
            'books': forms.CheckboxSelectMultiple()
        }
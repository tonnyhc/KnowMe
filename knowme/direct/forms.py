from django import forms

from knowme.direct.models import Message


class DirectForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': "Message..."
            })
        }
        labels = {
            'text': ''
        }
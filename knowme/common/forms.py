from django import forms

from knowme.common.models import CommentReport, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': "Add comment...",
                'label': ''
            }),
        }
        labels = {
            'text': ''
        }


class CommentReportForm(forms.ModelForm):
    class Meta:
        model = CommentReport
        fields = ['text']


class SearchBarForm(forms.Form):
    profile_name = forms.CharField(
        max_length=50,
        required=False,
    )
    widgets = {
        'profile_name': forms.TextInput(
            attrs={
                'placeholder': "Search"
            }
        )
    }
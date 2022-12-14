from django import forms

from knowme.posts.models import Post, Report


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class PostAddForm(PostBaseForm):
    class Meta:
        model = Post
        exclude = ('profile', 'publish_date')


class PostEditForm(PostBaseForm):
    class Meta:
        model = Post
        exclude = ('photo', 'profile', 'publish_date')


class PostReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['text']

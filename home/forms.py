from django import forms
from .models import Post, Comment


class CreateUpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form_control'})
        }
        labels = {
            'body': 'متن را وارد کنید',
        }


class ReplayCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {
            'body': 'پاسخ',
        }


class SearchPostForm(forms.Form):
    search = forms.CharField(label='جستجو')
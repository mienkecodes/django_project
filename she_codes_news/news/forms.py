# news/forms.py
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import NewsStory, Comment


class StoryForm(forms.ModelForm):
    comment_content = forms.CharField(
        label='Comment',
        widget=forms.Textarea(attrs={'rows': 3})
    )
    class Meta:
        model = NewsStory
        fields = ['title', 'pub_date', 'content', 'image_url', 'tags']
        widgets = {
            'pub_date': forms.DateInput(
            format='%m/%d/%Y',
            attrs={
                'class':'form-control',
                'placeholder':'Select a date',
                'type':'date'
            }           
        ),       
    }

    def save(self, commit=True):
        story = super().save(commit=commit)

        user = get_user_model().objects.get(username='john')
        comment_content = self.cleaned_data.get('comment_content')

        if commit and user and comment_content:
            comment = Comment.objects.create(
                news_story=story,
                author=user,
                content=comment_content
        )
        
        return story
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
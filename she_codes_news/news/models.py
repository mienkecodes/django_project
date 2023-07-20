from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation


class NewsStory(models.Model):
    title = models.CharField(max_length=200)
    # author = models.CharField(max_length=200)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField()
    content = models.TextField()
    image_url = models.URLField(max_length=200, null=True)
    tags = TaggableManager()
    # Add the comments field
    comments = GenericRelation('Comment', related_query_name='news_story')


# (blank=True, null=True) - check if you want someone to add image - might want to set an image in background


class Comment(models.Model):
    news_story = models.ForeignKey(NewsStory, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.timestamp}"
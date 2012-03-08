import datetime

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'

    
    def __unicode__(self):
        return self.title

class Comment(models.Model):
    poll = models.ForeignKey(Post)
    comment = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.comment

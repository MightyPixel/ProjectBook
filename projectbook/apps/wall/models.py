from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=150)
    body = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.question

class Comment(models.Model):
    poll = models.ForeignKey(Post)
    comment = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.comment

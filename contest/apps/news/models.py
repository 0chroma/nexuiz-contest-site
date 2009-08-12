from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(maxlength=200)
    author = models.ForeignKey(User)
    pub_date = models.DateField('Date Published')
    content = models.TextField('Content')
    class Admin:
        pass

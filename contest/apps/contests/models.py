from django.db import models
from django.contrib.auth.models import User

class Contest(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(maxlength=200)
    start_date = models.DateField('Start date')
    end_date = models.DateField('End date')
    judge_date = models.DateField('Judging Deadline')
    description = models.TextField('Description')
    
    class Admin:
        pass

class Entry(models.Model):
    def __str__(self):
        return self.title
    contest = models.ForeignKey(Contest)
    title = models.CharField(maxlength=200)
    disqualified = models.BooleanField("Disqualified", default=False)
    map = models.FileField("map", "Map pk3", "uploads")
    screenshot = models.ImageField("screenshot", "Screenshot", None, None, upload_to="uploads")
    user = models.ForeignKey(User)
    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        ordering = ('id',)
    class Admin:
        list_filter = ['contest']
    def get_score(self):
        scores = Score.objects.filter(entry=self)
        i = 0
        c = 0
        if scores:
            for score in scores:
                i += score.get_average()
                c += 1
        if c != 0:
            return i/c
        else:
            return 0

class Score(models.Model):
    def __str__(self):
        avg = (self.gameplay_score + self.visuals_score)/2
        return "%s from %s" % (avg, self.user)
    entry = models.ForeignKey(Entry)
    visuals_score = models.PositiveIntegerField()
    gameplay_score = models.PositiveIntegerField()
    comments = models.TextField("Comments")
    user = models.ForeignKey(User) 
    ", default=request.user.username, editable=False"
    def get_average(self):
        return (self.gameplay_score + self.visuals_score)/2
    class Admin:
        pass
from django.db import models

class Message(models.Model):
    uuid = models.CharField(max_length=32)
    text = models.TextField()
    deleted = models.BooleanField(default=False)
    why_deleted = models.TextField(blank=True)

    def __unicode__(self):
        return self.uuid


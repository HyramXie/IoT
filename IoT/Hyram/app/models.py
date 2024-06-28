from django.db import models
from datetime import datetime


# Create your models here.

class BaseModel(models.Model):
    class Meta:
        abstract = True

    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, **kwargs):
        self.deleted_at = datetime.now()
        self.save()


class Information(BaseModel):
    humidity = models.FloatField()
    temperature = models.FloatField()
    moisture = models.FloatField()

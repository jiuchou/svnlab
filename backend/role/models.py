from django.db import models

# Create your models here.
class Role(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    path = models.CharField(max_length=300, blank=True, null=True)
    module = models.CharField(max_length=50, blank=True, null=True)
    manager = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'role'

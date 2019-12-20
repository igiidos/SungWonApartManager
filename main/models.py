from django.conf import settings
from django.db import models


widths = (
    ('s', 'small'),
    ('m', 'midium'),
    ('l', 'large')
)


class SungWonSettings(models.Model):
    key_name = models.CharField(max_length=1, choices=widths)
    price = models.IntegerField()


class SungWonList(models.Model):
    article_num = models.IntegerField()
    size = models.IntegerField()
    dong = models.CharField(max_length=10)
    where = models.CharField(max_length=10)
    price = models.IntegerField()
    owner = models.CharField(max_length=10, blank=True) # OWNER or DOC
    office = models.CharField(max_length=100, blank=True)
    trade = models.CharField(max_length=1, blank=True) # Y or N
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.CharField(max_length=1, choices=(('y', 'yes'), ('n', 'no')), default='y')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)


class MyApplyList(models.Model):
    whose = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_apply_whose')
    apart = models.ForeignKey(SungWonList, on_delete=models.CASCADE, related_name='my_apply_apart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



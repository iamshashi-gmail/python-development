# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    task = models.CharField(max_length = 180)
    language=models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    completed = models.BooleanField(default = False, blank = True)
    

    def __str__(self):
        return self.task
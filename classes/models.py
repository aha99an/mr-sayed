from django.db import models


class Week(models.Model):

    name = models.CharField(max_length=200)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Class(models.Model):

    name = models.CharField(max_length=200)
    week = models.ForeignKey(
        Week, on_delete=models.CASCADE, related_name="week_class")
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

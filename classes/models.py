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
    DAYS_OF_WEEK = (
        (0, 'السبت'),
        (1, 'الأحد'),
        (2, 'الاثنين'),
        (3, 'الثلاثاء'),
        (4, 'الاربعاء'),
        (5, 'الخميس'),
        (6, 'الجمعة'),
    )

    name = models.CharField(max_length=200, null=True, blank=True)
    week = models.ForeignKey(
        Week, on_delete=models.CASCADE, related_name="week_class", null=True, blank=True)
    week_day = models.IntegerField(
        choices=DAYS_OF_WEEK, null=True, blank=True)
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


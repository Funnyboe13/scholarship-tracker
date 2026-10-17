from django.conf import settings
from django.db import models


class Scholarship(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not started'),
        ('in_progress', 'In progress'),
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scholarships',
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    deadline = models.DateField()
    coverage = models.CharField(max_length=100, help_text="e.g. Fully funded, 50%")
    link = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['deadline']

    def __str__(self):
        return self.name
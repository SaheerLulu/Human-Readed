from django.db import models

class EntryExitCount(models.Model):
    ENTRY_EXIT_CHOICES = (
        ('Entry', 'Entry'),
        ('Exit', 'Exit'),
    )
    type = models.CharField(max_length=10, choices=ENTRY_EXIT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)


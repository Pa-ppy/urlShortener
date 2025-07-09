from django.db import models

class URL(models.Model):
    original_url = models.URLField(unique=True, max_length=2048)
    short_code = models.CharField(max_length=15, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.original_url} -> {self.short_code}"
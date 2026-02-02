from django.db import models
from django.contrib.auth import get_user_model
from core.apps.courses.models import Course
User = get_user_model()

class Review(models.Model):
    STAR_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField(choices=STAR_CHOICES)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')  
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} → {self.course} ({self.rating})"


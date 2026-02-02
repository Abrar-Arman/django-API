from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES,default='beginner')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    



    
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()
    video_file = models.FileField(upload_to='videos/')
    document_file = models.FileField(upload_to='documents/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enroll(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),  
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} → {self.course} ({self.status})"


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')  

    def __str__(self):
        return f"{self.user} completed {self.lesson.title}"

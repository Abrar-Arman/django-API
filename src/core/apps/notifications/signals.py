from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from core.apps.courses.models import Enroll
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Enroll)
def send_enrollment_notification(sender, instance, created, **kwargs):
    
    if not created and instance.status == "confirmed":
        print("Signal triggered for enrollment:", instance.id)

        course = instance.course
        student = instance.user
        channel_layer = get_channel_layer()
        print(" channel_layer", channel_layer)

        recipients = []
        if course.created_by:
            recipients.append(course.created_by) 
        admin = User.objects.filter(role="admin").first()
        if admin:
            recipients.append(admin) 
       
        message = f"{student.username}'s enrollment in {course.title} course"

        for recipient in recipients:
            Notification.objects.create(
                recipient=recipient,
                message=message,
                course=course
            )

            try:
                async_to_sync(channel_layer.group_send)(
                    f"user_{recipient.id}",
                    {"type": "send_notification", "message": message}
                )
            except Exception as e:
                print("Channels notification skipped:", e)


          
    

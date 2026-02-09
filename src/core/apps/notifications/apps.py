from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = "core.apps.notifications"
    def ready(self):
        import core.apps.notifications.signals

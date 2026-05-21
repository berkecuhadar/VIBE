from django.apps import AppConfig

class VibeConfig(AppConfig):
    """
    Configuration class for the 'VIBE' application.
    Explicitly registers and wakes up model lifestyle receivers/signals upon framework startup.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vibe'

    def ready(self):
        """
        The ready() method is executed exactly once when Django initializes.
        Importing signals here hooks up event listeners securely without causing import loops.
        """
        import vibe.signals  # Safely importing and initializing the framework signals layer
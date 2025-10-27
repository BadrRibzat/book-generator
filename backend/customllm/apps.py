from django.apps import AppConfig


class CustomllmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customllm'
    verbose_name = 'Custom LLM Integration'

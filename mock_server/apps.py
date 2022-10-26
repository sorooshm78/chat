from django.apps import AppConfig


class MockServerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mock_server"

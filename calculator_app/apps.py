from django.apps import AppConfig


class CalculatorAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calculator_app'
    def ready(self):
        import calculator_app.signals
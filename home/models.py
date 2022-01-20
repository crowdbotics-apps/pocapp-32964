from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

APP_TYPES = (
    ("0", 'Web'),
    ("1", 'Mobile')
)
FRAMEWORKS = (
    ("0", 'Django'),
    ("1", 'React Native'),
)

PLAN_TYPE = (
    ("0", "Free"),
    ("10", "Standard"),
    ("25", "Pro")
)


class App(models.Model):
    domain_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(choices=APP_TYPES, max_length=25)
    framework = models.CharField(choices=FRAMEWORKS, max_length=25)
    description = models.TextField(blank=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    screenshot = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.domain_name}-{self.user}"


class Plan(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(choices=PLAN_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}-{self.price}"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.OneToOneField(App, on_delete=models.CASCADE)
    plan = models.OneToOneField(Plan, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('app', 'plan',)

    def __str__(self):
        return f"{self.user}-{self.app}-{self.plan}"

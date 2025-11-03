from django.db import models
from django.contrib.auth.models import User

class ActivityLog(models.Model):
    """
    Represents a single carbon-emitting activity logged by a user.
    """
    CATEGORY_CHOICES = [
        ('transport', 'Transport'),
        ('electricity', 'Electricity'),
        ('food', 'Food'),
        ('waste', 'Waste'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    value = models.FloatField(help_text="Input value, e.g., km, kWh, kg")
    carbon_equivalent = models.FloatField(editable=False, help_text="Calculated CO2 equivalent in kg")

    def __str__(self):
        """
        String representation of the ActivityLog object.
        """
        return f"{self.user.username} - {self.date}"

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ['-date']
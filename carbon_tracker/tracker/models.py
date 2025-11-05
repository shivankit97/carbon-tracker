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


class Goal(models.Model):
    """
    Represents a user's carbon footprint goal for a specific month.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    month = models.DateField(help_text="First day of the month for the goal.")
    target_footprint = models.FloatField(help_text="Target CO2 in kg.")

    def __str__(self):
        return f"{self.user.username}'s goal for {self.month.strftime('%B %Y')}: {self.target_footprint} kg CO2"

    class Meta:
        unique_together = ('user', 'month')
        ordering = ['-month']
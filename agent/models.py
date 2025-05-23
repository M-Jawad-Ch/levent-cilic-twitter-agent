from django.db import models
from django.core.validators import RegexValidator, MinValueValidator


class Tweet(models.Model):

    twitter_id = models.CharField(
        max_length=32,
        unique=True,
        validators=[RegexValidator(r"^\d+$", "Enter a valid numeric Tweet ID")],
    )
    content = models.CharField(max_length=25_000)
    tweeted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-tweeted_at"]


class BotStatus(models.Model):
    is_active = models.BooleanField(default=False)
    interval_minutes = models.PositiveIntegerField(
        default=90,
        validators=[MinValueValidator(90)],
        help_text="Tweeting interval in minutes (minimum 90)"
    )
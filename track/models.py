# models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Client(models.Model):
    name = models.CharField(max_length=200)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Worker(models.Model):
    name = models.CharField(max_length=200)
    worker_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} ({self.worker_id})"


class TimeEntry(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    date = models.DateField()
    invoice = models.ForeignKey('Invoice', null=True, blank=True, on_delete=models.SET_NULL)

    def get_duration(self):
        duration = self.end_time - self.start_time
        return duration.total_seconds() / 3600  # Convert to hours

    def get_amount(self):
        return self.get_duration() * self.client.hourly_rate

    class Meta:
        ordering = ['-date', '-start_time']


class Invoice(models.Model):
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    date = models.DateField()
    invoice_day = models.IntegerField(choices=WEEKDAY_CHOICES, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_hours = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-date']

    @staticmethod
    def get_next_invoice_date(weekday):
        today = timezone.now().date()
        days_ahead = weekday - today.weekday()
        if days_ahead <= 0:
            days_ahead += 14  # Next occurrence in 2 weeks
        return today + timedelta(days=days_ahead)

    def calculate_totals(self):
        entries = TimeEntry.objects.filter(invoice=self)
        total_amount = sum(entry.get_amount() for entry in entries)
        total_hours = sum(entry.get_duration() for entry in entries)

        self.total_hours = total_hours
        self.total_amount = total_amount
        self.save()
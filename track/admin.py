from django.contrib import admin
from .models import Client, Worker, TimeEntry, Invoice

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'hourly_rate')
    search_fields = ('name',)

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'worker_id')
    search_fields = ('name', 'worker_id')

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'client', 'worker', 'get_duration', 'get_amount')
    list_filter = ('client', 'worker', 'date')
    search_fields = ('description',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_amount', 'total_hours')
    list_filter = ('date',)
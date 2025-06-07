from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
from django.utils import timezone

from .models import TimeEntry, Invoice
from .forms import TimeEntryFilterForm, TimeEntryForm


class TimeEntryListView(LoginRequiredMixin, ListView):
    model = TimeEntry
    template_name = 'timeentry_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        queryset = TimeEntry.objects.filter(invoice__isnull=True)

        form = TimeEntryFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['client']:
                queryset = queryset.filter(client=form.cleaned_data['client'])
            if form.cleaned_data['worker']:
                queryset = queryset.filter(worker=form.cleaned_data['worker'])
            if form.cleaned_data['date_from']:
                queryset = queryset.filter(date__gte=form.cleaned_data['date_from'])
            if form.cleaned_data['date_to']:
                queryset = queryset.filter(date__lte=form.cleaned_data['date_to'])
            if form.cleaned_data['invoice_date']:
                queryset = queryset.filter(invoice__date=form.cleaned_data['invoice_date'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TimeEntryFilterForm(self.request.GET)

        entries = context['entries']
        context['total_hours'] = sum(entry.get_duration() for entry in entries)
        context['total_amount'] = sum(entry.get_amount() for entry in entries)

        return context


class TimeEntryCreateView(LoginRequiredMixin, CreateView):
    model = TimeEntry
    form_class = TimeEntryForm
    template_name = 'track/timeentry_form.html'
    success_url = '/'

    def get_initial(self):
        initial = super().get_initial()
        initial['date'] = timezone.now().date()
        initial['start_time'] = timezone.now()
        initial['end_time'] = timezone.now()
        return initial


class TimeEntryUpdateView(LoginRequiredMixin, UpdateView):
    model = TimeEntry
    form_class = TimeEntryForm
    template_name = 'track/timeentry_form.html'
    success_url = '/'


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'invoice_list.html'
    context_object_name = 'invoices'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем активный инвойс
        latest_invoice = self.get_queryset().first()

        if latest_invoice:
            # Для таблицы клиентов
            client_stats = TimeEntry.objects.filter(invoice=latest_invoice) \
                .values('client__name') \
                .annotate(
                total_hours=Sum(F('end_time') - F('start_time')),
                total_amount=Sum(F('client__hourly_rate') * (F('end_time') - F('start_time')))
            )

            # Для таблицы работников
            worker_stats = TimeEntry.objects.filter(invoice=latest_invoice) \
                .values('worker__name') \
                .annotate(
                total_hours=Sum(F('end_time') - F('start_time')),
                total_amount=Sum(F('client__hourly_rate') * (F('end_time') - F('start_time')))
            )

            context.update({
                'client_stats': client_stats,
                'worker_stats': worker_stats,
                'next_invoice_date': Invoice.get_next_invoice_date(latest_invoice.invoice_day)
            })

        return context

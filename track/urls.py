from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'track'

urlpatterns = [
    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # Time Entries URLs
    path('', views.TimeEntryListView.as_view(), name='timeentry_list'),
    path('entry/create/', views.TimeEntryCreateView.as_view(), name='timeentry_create'),
    path('entry/<int:pk>/update/', views.TimeEntryUpdateView.as_view(), name='timeentry_update'),

    # Invoice URLs
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
]
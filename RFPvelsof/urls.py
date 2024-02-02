from django.urls import path
from RFPapp.views import admin_registration, vendor_registration, login_view, dashboard_vendors, approve_vendor, \
    logout_view, dashboard, edit_vendor_view

urlpatterns = [
    path('', login_view, name='login'),
    path('admin-registration/', admin_registration, name='admin_registration'),
    path('vendor-registration/', vendor_registration, name='vendor_registration'),
    path('dashboard/vendors', dashboard_vendors, name='dashboard_vendors'),
    path('edit_vendor/<int:vendor_id>/', edit_vendor_view, name='edit_vendor'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('approve_vendor/<int:vendor_id>/', approve_vendor, name='approve_vendor'),
]

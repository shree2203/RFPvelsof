from django.urls import path
from RFPapp.views import admin_registration, vendor_registration, login_view, dashboard_vendors, approve_vendor, \
    logout_view, dashboard, edit_vendor_view, rfp_list_view, add_rfp, select_category, close_rfp

urlpatterns = [
    path('', login_view, name='login'),
    path('admin-registration/', admin_registration, name='admin_registration'),
    path('vendor-registration/', vendor_registration, name='vendor_registration'),
    path('dashboard/vendors', dashboard_vendors, name='dashboard_vendors'),
    path('dashboard/rfp-list/', rfp_list_view, name='rfp_list'),
    path('edit_vendor/<int:vendor_id>/', edit_vendor_view, name='edit_vendor'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/add-rfp', add_rfp, name='add_rfp'),
    path('close-rfp/<int:rfp_id>/', close_rfp, name='close_rfp'),
    path('add-rfp/select-category/', select_category, name='select-category'),
    path('logout/', logout_view, name='logout'),
    path('approve_vendor/<int:vendor_id>/', approve_vendor, name='approve_vendor'),
]

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from RFPvelsof import settings
from .forms import LoginForm
from .models import VendorDetails, Approval, CustomUser
from django.core.mail import send_mail


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def edit_vendor_view(request, vendor_id):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        noofemployees = request.POST.get('noofemployees')
        revenue = request.POST.get('revenue')
        gstno = request.POST.get('gstno')
        panno = request.POST.get('panno')
        phnno = request.POST.get('phnno')
        categories = request.POST.get('Categories')
        try:
            vendor_details = VendorDetails.objects.get(id=vendor_id)
            user = vendor_details.user

            # Update user fields
            user.email = email
            user.first_name = firstname
            user.last_name = lastname
            user.is_approved_by_admin = False
            user.save()

            # Update vendor details fields
            vendor_details.revenue = revenue
            vendor_details.gst_no = gstno
            vendor_details.pan_no = panno
            vendor_details.phn_no = phnno
            vendor_details.total_employees = noofemployees
            vendor_details.categories = categories
            vendor_details.save()

        except CustomUser.DoesNotExist or VendorDetails.DoesNotExist:
            messages.error(request, 'User or Vendor details not found.')
            return render(request, 'edit_vendor.html', {'vendor_id': vendor_id})

    return render(request, 'edit_vendor.html', {'vendor_id': vendor_id})


def send_email(user_email, msg, sub):
    subject = sub
    message = msg
    from_email = settings.EMAIL_HOST_USER  # Update with your email address or use a configured email
    recipient_list = [user_email, ]
    send_mail(subject, message, from_email, recipient_list)


def login_view(request):
    messages = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user:
                if user.user_type == 'vendor' and not user.is_approved_by_admin:
                    messages = 'Your account is pending approval. Please wait for admin confirmation.'
                elif user.is_active:
                    login(request, user)
                    return redirect('/dashboard')
                else:
                    messages = 'Your account is disabled.'
            else:
                messages = 'Invalid login credentials.'

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'messages': messages})


def admin_registration(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if password != confirmpassword:
            messages.error(request, 'password does not match')
            return render(request, 'admin_registration.html')
        try:
            user = CustomUser.objects.create_user(email=email, password=password, first_name=firstname,
                                                  last_name=lastname)
            user.user_type = 'admin'
            user.save()
        except Exception as e:
            messages.error(request, f'{e}')
            return render(request, 'admin_registration.html')

        return redirect('login')
    return render(request, 'admin_registration.html')


def vendor_registration(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        noofemployees = request.POST.get('noofemployees')
        revenue = request.POST.get('revenue')
        gstno = request.POST.get('gstno')
        panno = request.POST.get('panno')
        phnno = request.POST.get('phnno')
        categories = request.POST.get('Categories')
        if password != confirmpassword:
            messages.error(request, 'password does not match')
            return render(request, 'vendor_registration.html')
        try:
            user = CustomUser.objects.create_user(email=email, password=password, first_name=firstname,
                                                  last_name=lastname)
            user.user_type = 'vendor'
            user.save()
            # Create VendorDetails entry
            vendor_details = VendorDetails(user=user, revenue=revenue, gst_no=gstno, pan_no=panno, phn_no=phnno,
                                           total_employees=noofemployees, categories=categories)
            vendor_details.save()
            # Create Approval entry (not approved by default)
            approval = Approval(vendor=vendor_details)
            approval.save()
            msg = (f'Hi {firstname},'
                   f'Thanks for showing registration on our RFP System. '
                   'We will review the details & approve the account shortly.Thanks Velocity RFP System')
            sub = 'Registration Confirmation - Velocity RFP System'
            send_email(email, msg, sub)
        except Exception as e:
            messages.error(request, f'{e}')
            return render(request, 'vendor_registration.html')

        return redirect('login')

    return render(request, 'vendor_registration.html')


@login_required()
def dashboard_vendors(request):
    vendors = VendorDetails.objects.all().exclude(user__is_approved_by_admin=True)
    return render(request, 'dashboard.html', {'vendors': vendors, 'table': True})


@login_required()
def dashboard(request):
    return render(request, 'dashboard.html', {'table': False})


@login_required()
def approve_vendor(request, vendor_id):
    vendor = VendorDetails.objects.get(pk=vendor_id)
    obj = CustomUser.objects.get(email=vendor.user.email)
    obj.is_approved_by_admin = True
    obj.save()
    msg = f'Thanks for showing interest on our RFP System. Your account has been approved'
    sub = 'Registration Approved'
    email = vendor.user.email
    send_email(email, msg, sub)
    prompt = f"Approval Email has been sent to {vendor.user.first_name}"
    vendors = VendorDetails.objects.exclude(pk=vendor_id).exclude(user__is_approved_by_admin=True)
    return render(request, 'dashboard.html', {'prompt': prompt, 'vendors': vendors})

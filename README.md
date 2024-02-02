# RFP System

Welcome to the RFP System, a web application for managing Requests for Proposals and vendor approvals.

## Overview

The RFP System provides a platform for users to create and manage Requests for Proposals, while allowing administrators to review and approve vendor registrations. The system includes features for user authentication, admin approval workflow, and vendor details management.

## Features

- **User Authentication:** Secure login and registration for Admin and Vendors.

- **Admin Registration:** Separate registration for Admin users with a dedicated registration page.

- **Vendor Registration:** Vendors register through a dedicated registration page and require admin approval.

- **Approval Workflow:** Vendors can't log in until approved by the admin.

- **Vendor Details Management:** Admins can review and approve vendor details, including additional information required for registration.

## Setup

1. Clone the repository:

    ```bash
    git clone git@github.com:shree2203/RFPvelsof.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Put your email and App password in the settings file to send mail
   
       EMAIL_HOST_USER = ' '
       EMAIL_HOST_PASSWORD = ' '

3. Run migrations:

    ```bash
    python manage.py migrate
    ```

4. Create a superuser for admin access:

    ```bash
    python manage.py createsuperuser
    ```

5. Start the development server:

    ```bash
    python manage.py runserver
    ```

6. Open the application in your web browser: [http://localhost:8000/](http://localhost:8000/)

## Usage

- Access the admin panel at [http://localhost:8000/admin/](http://localhost:8000/admin/) using the superuser credentials.

- Use the provided Django admin interface to manage users, vendor details, and approvals.

- Users can log in using their credentials, and vendors need admin approval before logging in.


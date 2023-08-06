# crouber_user-api

[![Actions Status](https://github.com/Ngwo-Labs/crouber_user-api/workflows/CI%20Test/badge.svg)](https://github.com/Ngwo-Labs/crouber_user-api/actions)

A reusable django application which provides the user api features of the Crouber web application

Features include:

    * Token authentication

    * user profile management

Quick start
-----------

1. Add "user_api", "profile_api" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [
        ...
    'user_api.apps.UserApiConfig',
    'profile_api.apps.ProfileApiConfig',
    ]
   Note: Install/download the crouber-user-api package before doing this step
2. Include the users URLconf in your project urls.py like this:

    path('users/', include('user_api.urls')),

3. Run ``python manage.py migrate`` to create the users models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a user (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/users/ to manage or create a users.

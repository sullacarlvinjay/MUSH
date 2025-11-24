#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    username = 'admin'
    email = 'admin@mushguard.com'
    password = 'tucker11'
    
    try:
        if User.objects.filter(username=username).exists():
            # Update existing admin user's password
            admin_user = User.objects.get(username=username)
            admin_user.set_password(password)
            admin_user.save()
            print(f"Admin user '{username}' password updated to '{password}'!")
        else:
            # Create new admin user
            User.objects.create_superuser(username, email, password)
            print(f"Admin user '{username}' created successfully!")
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
        return False
    return True

if __name__ == '__main__':
    success = create_admin()
    if success:
        print("Admin setup completed successfully!")
    else:
        print("Admin setup failed!")
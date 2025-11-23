from django.http import HttpResponse
from django.contrib.auth.models import User

def create_admin_now(request):
    """Create admin user immediately when this URL is visited."""
    username = 'admin'
    email = 'admin@mushguard.com'
    password = 'admin123'
    
    try:
        # Check existing users
        existing_users = User.objects.all()
        users_list = [f"{u.username} (superuser: {u.is_superuser}, staff: {u.is_staff})" for u in existing_users]
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            message = f"✅ Admin user created!<br>Username: {username}<br>Password: {password}<br><a href='/admin/'>Go to Admin</a>"
        else:
            user = User.objects.get(username=username)
            message = f"ℹ️ Admin user already exists.<br>Username: {username}<br>Password: {password}<br>Superuser: {user.is_superuser}<br>Staff: {user.is_staff}<br><a href='/admin/'>Go to Admin</a>"
        
        return HttpResponse(f"""
        <html>
        <head><title>Admin Created</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>MushGuard Admin Setup</h2>
            <div style="background: #f0f8ff; padding: 20px; border-radius: 8px; display: inline-block;">
                {message}
                <hr>
                <h3>All Users in Database:</h3>
                <div style="text-align: left; background: #f9f9f9; padding: 10px; border-radius: 4px;">
                    {'<br>'.join(users_list) if users_list else 'No users found'}
                </div>
            </div>
        </body>
        </html>
        """)
    except Exception as e:
        return HttpResponse(f"❌ Error: {str(e)}")

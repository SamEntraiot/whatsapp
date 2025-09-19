#!/usr/bin/env python
"""
Setup script for WhatsApp  Django project
"""
import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def run_command(command, description):
    """Run a command and print status"""
    print(f"\n🔄 {description}...")
    try:
        if isinstance(command, list):
            result = subprocess.run(command, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def setup_django():
    """Setup Django project"""
    print("🚀 Setting up WhatsApp Clone Django Project")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whatsapp_clone.settings')
    
    # Install requirements
    if not run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      "Installing Python dependencies"):
        return False
    
    # Setup Django
    django.setup()
    
    # Make migrations
    if not run_command([sys.executable, 'manage.py', 'makemigrations'], 
                      "Creating database migrations"):
        return False
    
    # Run migrations
    if not run_command([sys.executable, 'manage.py', 'migrate'], 
                      "Applying database migrations"):
        return False
    
    # Create sample users
    print("\n🔄 Creating sample users...")
    try:
        from django.contrib.auth.models import User
        
        # Create sample users if they don't exist
        users_data = [
            {'username': 'alice', 'password': 'testpass123', 'email': 'alice@example.com'},
            {'username': 'bob', 'password': 'testpass123', 'email': 'bob@example.com'},
            {'username': 'charlie', 'password': 'testpass123', 'email': 'charlie@example.com'},
        ]
        
        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(**user_data)
                print(f"✅ Created user: {user_data['username']}")
            else:
                print(f"ℹ️  User {user_data['username']} already exists")
                
    except Exception as e:
        print(f"❌ Error creating sample users: {e}")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start Redis server: redis-server")
    print("2. Run Django server: python manage.py runserver")
    print("3. Visit http://127.0.0.1:8000")
    print("\n👥 Sample users created:")
    print("   - alice / testpass123")
    print("   - bob / testpass123") 
    print("   - charlie / testpass123")
    
    return True

if __name__ == '__main__':
    setup_django()

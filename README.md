# WhatsApp Clone - Django + WebSocket

A real-time chat application built with Django, Django Channels, and Redis that mimics WhatsApp's interface and functionality.

## Features

- **Real-time messaging** using WebSockets
- **1-to-1 direct chats**
- **WhatsApp-like UI** with modern design
- **Typing indicators**
- **Message history**
- **User authentication**
- **Responsive design**

## Tech Stack

- **Backend**: Django 4.2.7
- **WebSocket**: Django Channels 4.0.0
- **Channel Layer**: Redis (channels-redis)
- **Database**: SQLite (can be changed to PostgreSQL/MySQL)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)

## Prerequisites

- Python 3.8+
- Redis server
- pip (Python package manager)

## Installation & Setup

### 1. Install Redis (Optional but Recommended)

**Windows:**
- **Option 1**: Download from https://github.com/microsoftarchive/redis/releases
- **Option 2**: Use WSL: `wsl sudo apt-get install redis-server`
- **Option 3**: Use Docker: `docker run -d -p 6379:6379 redis:alpine`
- **Option 4**: Run `start_redis.bat` (if Redis is installed)

**macOS:**
```bash
brew install redis
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install redis-server
```

**Note**: The app will work without Redis using in-memory channels, but real-time features will only work within a single server instance.

### 2. Clone and Setup Project

```bash
# Navigate to project directory
cd WhatsApp

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 4. Start Redis Server

```bash
# Start Redis server (keep this running)
redis-server
```

### 5. Run the Application

```bash
# Start Django development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## Usage

### 1. Register/Login
- Create a new account or login with existing credentials
- Multiple users can register to test chat functionality

### 2. Start Conversations
- **Direct Chat**: Click the "New Chat" icon and select a user to start a private conversation

### 3. Real-time Features
- Messages appear instantly without page refresh
- Typing indicators show when someone is typing
- Message timestamps are displayed

## Project Structure

```
WhatsApp/
├── manage.py
├── requirements.txt
├── README.md
├── whatsapp_clone/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── chat/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py      # WebSocket consumers
│   ├── models.py         # Conversation & Message models
│   ├── routing.py        # WebSocket URL routing
│   ├── views.py          # HTTP views
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
└── templates/
    ├── base.html
    └── chat/
        ├── login.html
        ├── register.html
        ├── chat_list.html
        └── chat_room.html
```

## Models

### Conversation
- Supports direct (1-to-1) chats only
- Many-to-many relationship with Users (limited to 2 participants)
- Tracks creation and update timestamps

### Message
- Belongs to a conversation
- Has sender, content, timestamp
- Includes read status tracking

## WebSocket Consumer

The `ChatConsumer` handles:
- Real-time message sending/receiving
- Typing indicators
- Message history loading
- User authentication checks

## API Endpoints

- `/` - Chat list (home page)
- `/login/` - User login
- `/register/` - User registration
- `/logout/` - User logout
- `/chat/<id>/` - Chat room
- `/start-conversation/` - Create new conversation
- `/api/conversations/` - Get conversations (JSON API)

## WebSocket Endpoints

- `ws/chat/<conversation_id>/` - WebSocket connection for real-time chat

## Configuration

### Redis Configuration
Edit `settings.py` to change Redis connection:

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # Change host/port as needed
        },
    },
}
```

### Database Configuration
To use PostgreSQL instead of SQLite:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'whatsapp_clone',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Testing

Run the test suite:

```bash
python manage.py test
```

## Deployment Considerations

For production deployment:

1. **Use a production ASGI server** like Daphne or Uvicorn
2. **Configure Redis** for production (Redis Cluster for high availability)
3. **Use PostgreSQL** instead of SQLite
4. **Set DEBUG = False** in settings
5. **Configure static files** serving
6. **Use environment variables** for sensitive settings
7. **Set up SSL/TLS** for WebSocket security (WSS)

## Troubleshooting

### Common Issues

1. **Redis Connection Error**
   - Ensure Redis server is running
   - Check Redis host/port configuration

2. **WebSocket Connection Failed**
   - Check if Daphne is running
   - Verify ASGI configuration
   - Check browser console for errors

3. **Messages Not Appearing**
   - Check WebSocket connection status
   - Verify user permissions for conversation
   - Check Django logs for errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is for educational purposes. Feel free to use and modify as needed.

## Future Enhancements

- File/image sharing
- Message reactions
- Message search
- Push notifications
- Voice messages
- Video calling
- Message encryption
- User status (online/offline)
- Message delivery status
- Dark mode theme

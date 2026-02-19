# Django Event Management System

A fully functional Event Management System built with Django and Tailwind CSS. This application provides complete CRUD operations for managing events, participants, and categories with optimized database queries and a responsive user interface.

## Features

### 📊 Dashboard
- **Statistics Overview**: View total participants, events, upcoming events, and past events
- **Today's Events**: Quick view of events scheduled for today
- **Interactive Stats Cards**: Clickable cards to filter events by status
- **Quick Actions**: Fast access to create events, participants, and categories

### 🎫 Event Management
- **Full CRUD Operations**: Create, Read, Update, and Delete events
- **Advanced Search**: Search events by name or location
- **Smart Filtering**:
  - Filter by category
  - Filter by date range
  - View upcoming or past events
- **Optimized Queries**: Uses `select_related()` and `prefetch_related()` for efficient database access
- **Participant Tracking**: View and manage participant lists for each event

### 👥 Participant Management
- **Complete Participant Records**: Manage participant information
- **Event Registration**: Associate participants with multiple events
- **Event Count Display**: See how many events each participant is registered for
- **Participant Details**: View all events a participant is attending

### 🏷️ Category Management
- **Event Categorization**: Organize events by categories
- **Event Count**: Track number of events per category
- **Direct Navigation**: Click to view all events in a category

### 🎨 User Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Tailwind CSS**: Modern, clean design with Tailwind CSS via CDN
- **Mobile Navigation**: Hamburger menu for small screens
- **Success Messages**: Visual feedback for all CRUD operations
- **Form Validation**: Client and server-side validation

## Technology Stack

- **Backend**: Django 6.0.2
- **Frontend**: Tailwind CSS (via CDN)
- **Database**: SQLite (default, easily configurable for PostgreSQL/MySQL)
- **Python**: 3.12+

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ahemon369/Django-Assignment-01.git
   cd Django-Assignment-01
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
Django-Assignment-01/
├── event_management/          # Project settings
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── events/                    # Main application
│   ├── migrations/           # Database migrations
│   ├── templates/
│   │   └── events/          # HTML templates
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── event_*.html
│   │       ├── participant_*.html
│   │       └── category_*.html
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── apps.py
│   ├── forms.py             # Django forms
│   ├── models.py            # Data models
│   ├── urls.py              # App URL patterns
│   └── views.py             # View functions
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Database Models

### Category
- `name` (CharField, unique): Category name
- `description` (TextField): Category description

### Event
- `name` (CharField): Event name
- `description` (TextField): Event description
- `date` (DateField): Event date
- `time` (TimeField): Event time
- `location` (CharField): Event location
- `category` (ForeignKey): Related category

### Participant
- `name` (CharField): Participant name
- `email` (EmailField, unique): Participant email
- `events` (ManyToManyField): Registered events

## URL Patterns

### Main Pages
- `/` - Dashboard
- `/events/` - Event list
- `/participants/` - Participant list
- `/categories/` - Category list
- `/admin/` - Django admin panel

### Event URLs
- `/events/` - List all events (with search and filters)
- `/events/<id>/` - Event detail
- `/events/create/` - Create new event
- `/events/<id>/update/` - Update event
- `/events/<id>/delete/` - Delete event

### Participant URLs
- `/participants/` - List all participants
- `/participants/<id>/` - Participant detail
- `/participants/create/` - Create new participant
- `/participants/<id>/update/` - Update participant
- `/participants/<id>/delete/` - Delete participant

### Category URLs
- `/categories/` - List all categories
- `/categories/create/` - Create new category
- `/categories/<id>/update/` - Update category
- `/categories/<id>/delete/` - Delete category

## Query Optimization

The application implements several query optimization techniques:

1. **select_related()**: Used for ForeignKey relationships (Event → Category)
   ```python
   Event.objects.select_related('category')
   ```

2. **prefetch_related()**: Used for ManyToMany relationships (Event ↔ Participants)
   ```python
   Event.objects.prefetch_related('participants')
   ```

3. **Aggregate Queries**: Count participants across all events
   ```python
   Participant.objects.count()
   ```

4. **Annotate Queries**: Add computed fields like event count
   ```python
   Participant.objects.annotate(event_count=Count('events'))
   ```

## Features Demonstration

### Search Functionality
Search events by name or location:
```
/events/?q=Django
```

### Category Filtering
Filter events by category:
```
/events/?category=1
```

### Date Range Filtering
Filter events by date range:
```
/events/?start_date=2024-01-01&end_date=2024-12-31
```

### Status Filtering
View upcoming or past events:
```
/events/?filter=upcoming
/events/?filter=past
```

## Admin Interface

The Django admin panel is fully configured with:
- Searchable fields
- List filters
- Date hierarchy for events
- Horizontal filter for many-to-many relationships

## Development

### Adding Sample Data
```bash
python manage.py shell
```

Then run:
```python
from events.models import Category, Event, Participant
from datetime import date, time

# Create categories
tech = Category.objects.create(name="Technology", description="Tech events")

# Create events
Event.objects.create(
    name="Django Workshop",
    description="Learn Django",
    date=date.today(),
    time=time(10, 0),
    location="Tech Hub",
    category=tech
)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is created for educational purposes.

## Contact

For questions or support, please open an issue on GitHub.
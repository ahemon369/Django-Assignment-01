from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date
from .models import Category, Event, Participant
from .forms import CategoryForm, EventForm, ParticipantForm


def dashboard(request):
    """Dashboard view with statistics and today's events"""
    today = date.today()
    
    # Aggregate queries
    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_events_count = Event.objects.filter(date__gte=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()
    
    # Today's events
    todays_events = Event.objects.filter(date=today).select_related('category').prefetch_related('participants')
    
    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'todays_events': todays_events,
    }
    return render(request, 'events/dashboard.html', context)


# Event Views
def event_list(request):
    """List all events with optimized queries and filters"""
    today = date.today()
    events = Event.objects.select_related('category').prefetch_related('participants')
    
    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)
    
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        events = events.filter(date__gte=start_date)
    if end_date:
        events = events.filter(date__lte=end_date)
    
    # Filter by upcoming/past
    filter_type = request.GET.get('filter')
    if filter_type == 'upcoming':
        events = events.filter(date__gte=today)
    elif filter_type == 'past':
        events = events.filter(date__lt=today)
    
    # Annotate with participant count
    events = events.annotate(participant_count=Count('participants'))
    
    categories = Category.objects.all()
    
    context = {
        'events': events,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'filter_type': filter_type,
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    """Event detail view"""
    event = get_object_or_404(Event.objects.select_related('category').prefetch_related('participants'), pk=pk)
    context = {
        'event': event,
    }
    return render(request, 'events/event_detail.html', context)


def event_create(request):
    """Create a new event"""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    return render(request, 'events/event_form.html', context)


def event_update(request, pk):
    """Update an event"""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'action': 'Update',
        'event': event,
    }
    return render(request, 'events/event_form.html', context)


def event_delete(request, pk):
    """Delete an event"""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')
    
    context = {
        'event': event,
    }
    return render(request, 'events/event_confirm_delete.html', context)


# Participant Views
def participant_list(request):
    """List all participants"""
    participants = Participant.objects.prefetch_related('events').annotate(event_count=Count('events'))
    
    context = {
        'participants': participants,
    }
    return render(request, 'events/participant_list.html', context)


def participant_detail(request, pk):
    """Participant detail view"""
    participant = get_object_or_404(Participant.objects.prefetch_related('events'), pk=pk)
    
    context = {
        'participant': participant,
    }
    return render(request, 'events/participant_detail.html', context)


def participant_create(request):
    """Create a new participant"""
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant created successfully!')
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    return render(request, 'events/participant_form.html', context)


def participant_update(request, pk):
    """Update a participant"""
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant updated successfully!')
            return redirect('participant_detail', pk=pk)
    else:
        form = ParticipantForm(instance=participant)
    
    context = {
        'form': form,
        'action': 'Update',
        'participant': participant,
    }
    return render(request, 'events/participant_form.html', context)


def participant_delete(request, pk):
    """Delete a participant"""
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        messages.success(request, 'Participant deleted successfully!')
        return redirect('participant_list')
    
    context = {
        'participant': participant,
    }
    return render(request, 'events/participant_confirm_delete.html', context)


# Category Views
def category_list(request):
    """List all categories"""
    categories = Category.objects.annotate(event_count=Count('event'))
    
    context = {
        'categories': categories,
    }
    return render(request, 'events/category_list.html', context)


def category_create(request):
    """Create a new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    return render(request, 'events/category_form.html', context)


def category_update(request, pk):
    """Update a category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'action': 'Update',
        'category': category,
    }
    return render(request, 'events/category_form.html', context)


def category_delete(request, pk):
    """Delete a category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    
    context = {
        'category': category,
    }
    return render(request, 'events/category_confirm_delete.html', context)

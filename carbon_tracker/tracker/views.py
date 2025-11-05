from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from datetime import date
from .forms import ActivityLogForm, GoalForm
from .models import ActivityLog, Goal

def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from .utils import generate_chart_base64, generate_personalized_tips


@login_required
def dashboard(request):
    """
    Display user's dashboard with activity logs and carbon footprint summaries.
    """
    # Fetch all logs for the current user
    logs = ActivityLog.objects.filter(user=request.user)

    # Calculate total carbon footprint
    total_footprint = logs.aggregate(total=Sum('carbon_equivalent'))['total'] or 0

    # Calculate total footprint by category
    category_totals = (
        logs.values('category')
        .annotate(total=Sum('carbon_equivalent'))
        .order_by('category')
    )

    # Convert category totals to a more accessible dictionary format
    category_summary = {item['category'].capitalize(): item['total'] for item in category_totals}

    # Generate the chart
    chart_image = generate_chart_base64(category_summary)

    # Generate personalized tips
    tips = generate_personalized_tips(category_summary)

    # Calculate monthly footprint
    today = date.today()
    first_day_of_month = today.replace(day=1)
    monthly_logs = logs.filter(date__gte=first_day_of_month)
    monthly_footprint = monthly_logs.aggregate(total=Sum('carbon_equivalent'))['total'] or 0

    # Get the current month's goal
    current_goal = Goal.objects.filter(user=request.user, month=first_day_of_month).first()

    context = {
        'recent_logs': logs.order_by('-date')[:10],  # Pass last 10 logs
        'total_footprint': total_footprint,
        'monthly_footprint': monthly_footprint,
        'category_summary': category_summary,
        'chart_image': chart_image,
        'tips': tips,
        'current_goal': current_goal,
    }

    return render(request, 'dashboard.html', context)

@login_required
def add_activity(request):
    """
    Handle adding a new activity log and calculating its carbon equivalent.
    """
    if request.method == 'POST':
        form = ActivityLogForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user

            # Carbon calculation logic
            category = form.cleaned_data['category']
            value = form.cleaned_data['value']
            if category == 'transport':
                activity.carbon_equivalent = value * 0.21
            elif category == 'electricity':
                activity.carbon_equivalent = value * 0.45
            elif category == 'food':
                activity.carbon_equivalent = value * 5.0
            elif category == 'waste':
                activity.carbon_equivalent = value * 0.5
            else:
                activity.carbon_equivalent = 0  # Default or error case

            activity.save()
            return redirect('dashboard')
    else:
        form = ActivityLogForm()
    
    return render(request, 'add_activity.html', {'form': form})


@login_required
def delete_activity(request, activity_id):
    """
    Delete an activity log.
    """
    activity = get_object_or_404(ActivityLog, id=activity_id, user=request.user)
    if request.method == 'POST':
        activity.delete()
        return redirect('dashboard')
    return render(request, 'confirm_delete.html', {'activity': activity})


from django.http import HttpResponse
import csv

@login_required
def export_csv(request):
    """
    Handles the export of user's activity logs to a CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="my_footprint.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['Date', 'Category', 'Value', 'CO2 Equivalent (kg)'])

    # Write data rows
    logs = ActivityLog.objects.filter(user=request.user).order_by('date')
    for log in logs:
        writer.writerow([log.date, log.get_category_display(), log.value, log.carbon_equivalent])

    return response


@login_required
def set_goal(request):
    """
    Allow users to set their monthly carbon footprint goal.
    """
    today = date.today()
    first_day_of_month = today.replace(day=1)

    # Get or create a goal for the current user and month
    goal, created = Goal.objects.update_or_create(
        user=request.user,
        month=first_day_of_month,
        defaults={'target_footprint': 0}
    )

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # If a goal exists, pre-fill the form. Otherwise, show a blank form.
        if not created:
            form = GoalForm(instance=goal)
        else:
            form = GoalForm()

    return render(request, 'set_goal.html', {'form': form})

from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache

from .forms import ScholarshipForm
from .models import Scholarship


class CustomLoginView(LoginView):
    template_name = 'scholarships/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return response


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('scholarship_list')
    else:
        form = UserCreationForm()
    return render(request, 'scholarships/signup.html', {'form': form})


@never_cache
@login_required
def scholarship_list(request):
    status = request.GET.get('status', '')
    scholarships = Scholarship.objects.filter(user=request.user)
    if status:
        scholarships = scholarships.filter(status=status)

    scholarships = list(scholarships)
    today = date.today()
    for s in scholarships:
        s.urgency = ''
        if s.status in ('not_started', 'in_progress'):
            if s.deadline < today:
                s.urgency = 'overdue'
            elif s.deadline <= today + timedelta(days=7):
                s.urgency = 'soon'

    context = {
        'scholarships': scholarships,
        'status_choices': Scholarship.STATUS_CHOICES,
        'current_status': status,
    }
    return render(request, 'scholarships/list.html', context)


@never_cache
@login_required
def scholarship_create(request):
    if request.method == 'POST':
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            scholarship = form.save(commit=False)
            scholarship.user = request.user
            scholarship.save()
            messages.success(request, "Scholarship added.")
            return redirect('scholarship_list')
    else:
        form = ScholarshipForm()
    return render(request, 'scholarships/form.html', {'form': form, 'title': 'Add scholarship'})


@never_cache
@login_required
def scholarship_update(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ScholarshipForm(request.POST, instance=scholarship)
        if form.is_valid():
            form.save()
            messages.success(request, "Scholarship updated.")
            return redirect('scholarship_list')
    else:
        form = ScholarshipForm(instance=scholarship)
    return render(request, 'scholarships/form.html', {'form': form, 'title': 'Edit scholarship'})


@never_cache
@login_required
def scholarship_delete(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk, user=request.user)
    if request.method == 'POST':
        scholarship.delete()
        messages.success(request, "Scholarship deleted.")
        return redirect('scholarship_list')
    return render(request, 'scholarships/confirm_delete.html', {'scholarship': scholarship})
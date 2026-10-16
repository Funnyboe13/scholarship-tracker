from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .models import Scholarship
from .forms import ScholarshipForm


def scholarship_list(request):
    status = request.GET.get('status', '')
    scholarships = Scholarship.objects.all()
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


def scholarship_create(request):
    if request.method == 'POST':
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scholarship_list')
    else:
        form = ScholarshipForm()
    return render(request, 'scholarships/form.html', {'form': form, 'title': 'Add scholarship'})


def scholarship_update(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    if request.method == 'POST':
        form = ScholarshipForm(request.POST, instance=scholarship)
        if form.is_valid():
            form.save()
            return redirect('scholarship_list')
    else:
        form = ScholarshipForm(instance=scholarship)
    return render(request, 'scholarships/form.html', {'form': form, 'title': 'Edit scholarship'})


def scholarship_delete(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    if request.method == 'POST':
        scholarship.delete()
        return redirect('scholarship_list')
    return render(request, 'scholarships/confirm_delete.html', {'scholarship': scholarship})
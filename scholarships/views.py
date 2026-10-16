from django.shortcuts import render, redirect
from .models import Scholarship
from .forms import ScholarshipForm


def scholarship_list(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarships/list.html', {'scholarships': scholarships})


def scholarship_create(request):
    if request.method == 'POST':
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scholarship_list')
    else:
        form = ScholarshipForm()
    return render(request, 'scholarships/form.html', {'form': form, 'title': 'Add scholarship'})
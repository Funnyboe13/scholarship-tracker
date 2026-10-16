from django.shortcuts import render
from .models import Scholarship


def scholarship_list(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarships/list.html', {'scholarships': scholarships})
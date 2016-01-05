from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Course, Batch, User, Student, Mentor
from .forms import StudentRegistrationForm, MentorRegistrationForm

def index(request):
	return render(request, 'projects_app/index.html')

def registration(request):
	if request.method == 'POST':
		student_form = StudentRegistrationForm(request.POST)
		mentor_form = MentorRegistrationForm(request.POST)
		
		if student_form.is_valid():
			name = student_form.cleaned_data['student_name']
			
			try:
				user = User(user_name=name, password=student_form.cleaned_data['password1'])
				user.save()
				student = Student(student_name=name, roll_no=student_form.cleaned_data['roll_no'], semester=int(student_form.cleaned_data['sem']), email=student_form.cleaned_data['email'], course=student_form.cleaned_data['course'], batch=student_form.cleaned_data['batch'], user=user)
				student.save()
				return HttpResponse("Student registered")
			except:
				raise Http404("Student registration failed.")
			
		elif mentor_form.is_valid():
			name = mentor_form.cleaned_data['mentor_name']
			
			try:
				user = User(user_name=name, password=mentor_form.cleaned_data['password1'])
				user.save()
				mentor = Mentor(mentor_name=name, email=mentor_form.cleaned_data['email'], user=user)
				mentor.save()
				return HttpResponse("Mentor Registered.")
			except:
				raise Http404("Mentor registration failed.")

		else:
			return HttpResponse('forms are invalid.')

	else:
		student_form = StudentRegistrationForm()
		mentor_form = MentorRegistrationForm()

	return render(request, 'projects_app/registration.html', { 'student_form': student_form, 'mentor_form': mentor_form })
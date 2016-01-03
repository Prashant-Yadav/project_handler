from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Course, Batch, User, Student
from .forms import StudentRegistrationForm, MentorRegistrationForm

def index(request):
	return render(request, 'projects_app/index.html')

def registration(request):
	if request.method == 'POST':
		student_form = StudentRegistrationForm(request.POST)
		mentor_form = MentorRegistrationForm(request.POST)
		
		if student_form.is_valid():
			name = student_form.cleaned_data['student_name']
			student_roll_no = student_form.cleaned_data['roll_no']
			course = student_form.cleaned_data['course']
			sem = student_form.cleaned_data['sem']
			batch = student_form.cleaned_data['batch']
			email_id = student_form.cleaned_data['email']
			password = student_form.cleaned_data['password1']
			
			try:
				user = User(user_name=name, password=password)
				user.save()
				course = Course.objects.get(course_name=course)
				batch = Batch.objects.get(batch_name=batch)
				student = Student(student_name=name, roll_no=student_roll_no, semester=sem, email=email_id, course=course.id, batch=batch.id, user=user.id)
				student.save()
				return HttpResponse("Submission successful.")
			except:
				raise Http404("name=%s, roll_no=%s, course=%s, batch=%s, sem=%s, user=%s, user_id=%s, email=%s, password=%s" % (name, student_roll_no, course.id, batch.id, sem, user, user.id, email_id, password))
			
		elif mentor_form.is_valid():
			name = mentor_form.cleaned_data['mentor_name']
			email = mentor_form.cleaned_data['email']
			password = mentor_form.cleaned_data['password1']
			return HttpResponse('Mentor form')
		else:
			return HttpResponse('forms are invalid.')

	else:
		student_form = StudentRegistrationForm()
		mentor_form = MentorRegistrationForm()

	return render(request, 'projects_app/registration.html', { 'student_form': student_form, 'mentor_form': mentor_form })

from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponse, Http404
from django.template import loader, RequestContext
from django.contrib.auth import login as django_login, authenticate, logout as django_logout

from .models import Course, Batch, User, Student, Mentor
from .forms import StudentRegistrationForm, MentorRegistrationForm, AuthenticationForm


def index(request):
	return render(request, 'projects_app/index.html')

def header_info(request):
	return render(request, 'projects_app/header.html')

def footer_info(request):
	return render(request, 'projects_app/footer.html')

def registration(request):
	if request.method == 'POST':
		student_form = StudentRegistrationForm(request.POST)
		mentor_form = MentorRegistrationForm(request.POST)
		
		if student_form.is_valid():
			name = student_form.cleaned_data['student_name']
			
			try:
				user = User(email=student_form.cleaned_data['email'])
				user.set_password(student_form.cleaned_data['password1'])
				user.save()

				student = Student(student_name=name, roll_no=student_form.cleaned_data['roll_no'], semester=int(student_form.cleaned_data['sem']), course=student_form.cleaned_data['course'], batch=student_form.cleaned_data['batch'], user=user)
				student.save()

				user = authenticate(email=student_form.cleaned_data['email'], password=student_form.cleaned_data['password1'])
				if user is not None:
					if user.is_active:
						# Login user
						django_login(request, user)
						return HttpResponse("Student registered and Logged in")
					else:
						return HttpResponse('user is not active')
			except:
				raise Http404("Student registration failed.")
			
		elif mentor_form.is_valid():
			name = mentor_form.cleaned_data['mentor_name']
			
			try:
				user = User(email=mentor_form.cleaned_data['email'])
				user.set_password(mentor_form.cleaned_data['password1'])
				user.save()

				mentor = Mentor(mentor_name=name, user=user)
				mentor.save()

				user = authenticate(email=mentor_form.cleaned_data['email'], password=mentor_form.cleaned_data['password1'])
				if user is not None:
					if user.is_active:
						# Login user
						django_login(request, user)
						return HttpResponse("Mentor Registered and Logged in.")
			except:
				raise Http404("Mentor registration failed.")

		else:
			return HttpResponse('forms are invalid.')

	else:
		student_form = StudentRegistrationForm()
		mentor_form = MentorRegistrationForm()

	return render_to_response('projects_app/registration.html', 
							{
								'student_form': student_form, 'mentor_form': mentor_form 
								}, 
							context_instance=RequestContext(request)
							)


def login(request):
    """
    Log in view
    """
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
        	try:
        		user = authenticate(email=request.POST['email'], password=request.POST['password'])
        		if user is not None:
        			if user.is_active:
        				django_login(request, user)
        				return HttpResponse('Successfully logged in')
        			else:
        				return HttpResponse('user not active')
        		else:
        			return HttpResponse('user none')
        	except:
        		raise Http404('Login failed.')
            
    else:
        login_form = AuthenticationForm()
    return render_to_response('projects_app/login.html', {
        'form': login_form,
    }, context_instance=RequestContext(request))


def logout(request):
	'''
	Log out view
	'''
	django_logout(request)
	return HttpResponse('Logged out')
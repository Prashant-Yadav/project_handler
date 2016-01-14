
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader, RequestContext
from django.contrib.auth import ( login as django_login, 
								authenticate, 
								logout as django_logout)
from django.contrib.auth.decorators import login_required

from .models import Course, Batch, User, Student, Mentor, StudentProject, Project
from .forms import ( StudentRegistrationForm, 
					MentorRegistrationForm, 
					AuthenticationForm,
					ProjectRegistrationForm )


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

				student = Student(student_name=name, 
								roll_no=student_form.cleaned_data['roll_no'], 
								semester=int(student_form.cleaned_data['sem']), 
								course=student_form.cleaned_data['course'], 
								batch=student_form.cleaned_data['batch'], 
								user=user
								)
				student.save()

				user = authenticate(email=student_form.cleaned_data['email'], 
								password=student_form.cleaned_data['password1']
								)

				if user is not None:
					if user.is_active:
						# Login user
						django_login(request, user)
						return HttpResponseRedirect("/student")
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

				user = authenticate(email=mentor_form.cleaned_data['email'], 
									password=mentor_form.cleaned_data['password1']
									)

				if user is not None:
					if user.is_active:
						# Login user
						django_login(request, user)
						return HttpResponseRedirect("/mentor")
			except:
				raise Http404("Mentor registration failed.")

		else:
			return HttpResponse('forms are invalid.')

	else:
		student_form = StudentRegistrationForm()
		mentor_form = MentorRegistrationForm()

	return render_to_response('projects_app/registration.html', 
							{
								'student_form': student_form, 
								'mentor_form': mentor_form 
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
        	email = request.POST['email']
        	try:
        		user = authenticate(email=email, password=request.POST['password'])
        		if user is not None:
        			if user.is_active:
        				django_login(request, user)
        				user = User.objects.get(email=email)
        				
        				try:
        					student=user.student_set.get()
        					return HttpResponseRedirect("/student")
        				except:
        					try:
        						mentor = user.mentor_set.get()
        						return HttpResponseRedirect("/mentor")
        					except:
        						raise Http404("User does not exist.")
        		else:
        			return HttpResponseRedirect('/invalid_login')
        	except:
        		raise HttpResponseRedirect('/invalid_login')
            
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
	return HttpResponseRedirect('/')

@login_required
def student_profile(request):
	user = User.objects.get(email=request.user.email)

	student = user.student_set.get()
	try:
		project = StudentProject.objects.filter(student=student)
	except StudentProject.DoesNotExist:
		project = None
	context = { 'student': student, 'student_projects': project }

	return render(request, 'projects_app/student_profile.html', context)


@login_required
def mentor_profile(request):
	user = User.objects.get(email=request.user.email)
	try:
		mentor = user.mentor_set.get()
		context = { 'mentor': mentor }
		return render(request, 'projects_app/mentor_profile.html', context)
	except:
		raise Http404('Unable to detect student')

def invalid_login(request):
	pass

@login_required
def project_register(request):

	if request.method == 'POST':
		form = ProjectRegistrationForm(request.POST)
		if form.is_valid():
			try:
				project = Project(project_name=form.cleaned_data['project_name'],
								project_description=form.cleaned_data['project_description'],
								github_link=form.cleaned_data['github_link'],
								mentor=form.cleaned_data['mentor']
							)
				project.save()

				user = User.objects.get(email=request.user.email)
				student = user.student_set.get()
				
				student_project = StudentProject(student=student,
												project=project
												)
				student_project.save()

				return HttpResponseRedirect("/student")

			except :
				raise Http404("Project Registraion failed.")

	else:
		form = ProjectRegistrationForm()

	return render_to_response('projects_app/project_register.html',
							{
								'form': form,
							},
							context_instance=RequestContext(request)
						)
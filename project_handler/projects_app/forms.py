
from django import forms

from .models import Course, Batch, User, Mentor


class StudentRegistrationForm(forms.Form):
	student_name = forms.CharField(label="Full Name", max_length="50")
	
	roll_no = forms.CharField(label="Roll No", max_length="12")

	course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Course")

	sem = forms.ChoiceField(choices=(
										(1, 'sem 1'),
										(2, 'sem 2'),
										(3, 'sem 3'),
										(4, 'sem 4'),
										(5, 'sem 5'),
										(6, 'sem 6'),
										(7, 'sem 7'),
										(8, 'sem 8'),
										(9, 'sem 9'),
										(10, 'sem 10'),
										(11, 'sem 11'),
										(12, 'sem 12'),
									)
								)

	batch = forms.ModelChoiceField(queryset=Batch.objects.all(), label="Batch")

	email = forms.EmailField()

	password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)))

	password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)))

	def clean(self):
		if ('password1' in self.cleaned_data) and ('password2' in self.cleaned_data):
			if (self.cleaned_data['password1']) != (self.cleaned_data['password2']):
				raise forms.ValidationError("The two password fields did not match.")
		return self.cleaned_data



class MentorRegistrationForm(forms.Form):
	mentor_name = forms.CharField(label="Full Name", max_length="50")

	email = forms.EmailField()

	password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)))

	password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)))

	def clean(self):
		if ('password1' in self.cleaned_data) and ('password2' in self.cleaned_data):
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError("The two password fields did not match.")
		return self.cleaned_data



class AuthenticationForm(forms.Form):
	
	# Login form
	email = forms.EmailField(widget=forms.widgets.TextInput)
	password = forms.CharField(widget=forms.widgets.PasswordInput)

	class Meta:
		fields = ['email', 'password']


class ProjectRegistrationForm(forms.Form):

	# Form for registering student project
	project_name = forms.CharField(max_length="50")
	project_description = forms.CharField(widget=forms.Textarea())
	github_link = forms.URLField()
	mentor = forms.ModelChoiceField(queryset=Mentor.objects.all())


from django import forms

from .models import Student, Course, Batch, User


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


class MentorRegistrationForm(forms.Form):
	mentor_name = forms.CharField(label="Full Name", max_length="50")

	email = forms.EmailField()

	password1 = forms.CharField(label="Password", max_length="30")

	password2 = forms.CharField(label="Confirm Password", max_length="30")
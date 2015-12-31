from __future__ import unicode_literals

from django.db import models



class User(models.Model):
	# Detail of Users
	user_name = models.CharField(max_length=50)
	password = models.CharField(max_length=30)

class Batch(models.Model):
	# all batches have their unique identification
	# for example, IT-2K11
	batch_name = models.CharField(max_length=20)

class Course(models.Model):
	# Course details
	# for example, course_name = MCA
	course_name = models.CharField(max_length=30)

class ProjectDocument(models.Model):
	# Documents to be submitted
	document_name = models.CharField(max_length=30)



class Student(models.Model):
	# student details
	student_name = models.CharField(max_length=50)
	roll_no = models.CharField(max_length=12)
	semester = models.IntegerField()
	email = models.EmailField(max_length=50)
	course = models.ForeignKey(Course)		# Foreign Key to course model
	batch = models.ForeignKey(Batch)		# Foreign Key to Batch model
	user = models.ForeignKey(User)			# Identification of user credentials



class Mentor(models.Model):
	# Mentor details
	mentor_name = models.CharField(max_length=50)
	email = models.EmailField(max_length=40)
	user = models.ForeignKey(User)			# Foreign key to user model

class MentorReview(models.Model):
	# Reviews provided by mentor to any approved project
	review_detail = models.TextField
	mentor = models.ForeignKey(Mentor)		# Foreign key to mentor model

class Notice(models.Model):
	# Notice issued by mentor to any batch
	notice_purpose = models.TextField()
	notice_date = models.DateField()
	batch = models.ForeignKey(Batch)		# Foreign key to batch model
	mentor = models.ForeignKey(Mentor)		# Foreign key to mentor model



class Project(models.Model):
	# Project Details
	project_name = models.CharField(max_length=30)
	project_description = models.TextField()
	github_link = models.URLField()
	mentor = models.ForeignKey(Mentor)		# Foreign Key to Mentor model

class DisapprovedProject(models.Model):
	# Projects disapproved by mentor
	project = models.ForeignKey(Project)				# Foreign key to project model
	reason_of_disapproval = models.TextField()

class ApprovedProject(models.Model):
	# Projects approved by mentor
	project = models.ForeignKey(Project)
	mentor_review = models.ForeignKey(MentorReview)		# Foreign key to mentor_review model

class DocumentSubmission(models.Model):
	# Identify documents submitted for projects
	document = models.ForeignKey(ProjectDocument)
	approved_project = models.ForeignKey(ApprovedProject)		# Foreign Key to identify project for which document submitted



class StudentProject(models.Model):
	# Identify which student is working on which project
	# connect student model with project model
	student = models.ForeignKey(Student)	# Foreign Key to Student model
	project = models.ForeignKey(Project)	# Foreign Key to Project model

from .models import Candidate
from django import forms

class CandidateInfoForm(forms.ModelForm):
	# Form to collect the details of the firm
	class Meta:
		model = Candidate
		fields = '__all__'
		widgets = {
			'first_name' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'First Name',
			}),
			'last_name' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Last Name',
			}),
			'email' : forms.EmailInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Email',
			}),
			'gender' : forms.Select(attrs={
				'class' : 'form-control',
				'placeholder' : 'Gender',
			}),
			'nationality' : forms.Select(attrs={
				'class' : 'form-control',
				'placeholder' : 'Nationality',
			}),
			'city' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'City',
			}),
			'currency' : forms.Select(attrs={
				'class' : 'form-control',
				'placeholder' : 'Currency',
			}),
			'salary' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Salary',
			}),
			'job_title' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Current Job title',
			}),
			'company' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Current Company',
			}),
			'dept' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Current Department',
			}),
			'skills' : forms.Textarea(attrs={
				'class' : 'form-control',
				'placeholder' : 'Skills',
				'rows' : 2,
			}),
			'edu_level' : forms.Select(attrs={
				'class' : 'form-control',
				'placeholder' : 'Qualification',
			}),
			'course' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Course',
			}),
			'specialisation' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Specialisation',
			}),
			'institute' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Institute of graduation',
			}),
			'year_of_completion' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Year of completion',
			}),
			'country_of_edu' : forms.Select(attrs={
				'class' : 'form-control',
				'placeholder' : 'Country of Education',
			}),
			'dob' : forms.DateInput(attrs={
				'class' : 'form-control datepicker',
				'placeholder' : 'Date of Birth',
			}),
			'visa_status' : forms.Select(attrs={
				'class' : 'form-control',
				'placeholder' : 'Visa Status',
			}),
			'languages' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Languages known',
			}),
			'marital_status' : forms.RadioSelect(attrs={
				#'class' : 'custom-control-input',
				'placeholder' : 'Marital Status',
			}),
			'driving_license' : forms.RadioSelect(attrs={
				#'class' : 'form-control',
				'placeholder' : 'Driving License',
			}),
			'exp_remarks' : forms.Textarea(attrs={
				'class' : 'form-control',
				'placeholder' : 'Experience Remarks',
				'rows' : '3'
			}),
			'about' : forms.Textarea(attrs={
				'class' : 'form-control',
				'placeholder' : 'About Me',
				'rows' : '3'
			}),
			'profile_photo' : forms.FileInput()
		}

class CandidateRegForm(CandidateInfoForm):
	# Form for registering candidate
	class Meta(CandidateInfoForm.Meta):
		fields = ['first_name', 'last_name','email',]

class ProfileForm(CandidateInfoForm):
	work_exp_year = forms.IntegerField(
					widget=forms.TextInput(attrs={
						'class' : 'form-control',
						'placeholder' : 'Work Experience (Years)',
					}))
	work_exp_month = forms.IntegerField(
					widget=forms.TextInput(attrs={
						'class' : 'form-control',
						'placeholder' : 'Work Experience (Month)',
					}))
	class Meta(CandidateInfoForm.Meta):
		exclude = ['experience']

class FilterForm(forms.Form):
	keyword = forms.CharField(
		widget = forms.TextInput(attrs={
			'class' : 'form-control form-control-sm',
			'placeholder' : 'Keyword',
		})
	)
	location = forms.CharField(
		required = False,
		widget = forms.TextInput(attrs={
			'class' : 'form-control form-control-sm',
			'placeholder' : 'Location',
		})
	)
	job_types = [
		('Full Time', 'Full Time'),
		('Part Time', 'Part Time'),
		('Internship', 'Internship'),
		('Temporary', 'Temporary'),
	]
	job_type = forms.ChoiceField(
		choices = job_types,
		widget = forms.Select(attrs={
			'class' : 'form-control  form-control-sm',
			'placeholder' : 'Job Type',
		})
	)

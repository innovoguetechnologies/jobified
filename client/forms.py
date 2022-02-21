from .models import Client, Employee, Job, Schedule
from django import forms

class ClientInfoForm(forms.ModelForm):
	# Form to collect or update all client details
	class Meta:
		model = Client
		fields = '__all__'
		widgets = {
			'name' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Name',
			}),
			'address' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Address',
			}),
			'company_size' : forms.Select(attrs={
				'class' : 'form-control',
			}),
			'about' : forms.Textarea(attrs={
				'class' : 'form-control',
				'placeholder' : 'About the company',
				'rows' : 2,
				
			}),
			'logo' : forms.FileInput(attrs={
				'class' : 'custom-file-input',
			})
		}

class ClientRegForm(ClientInfoForm):
	# Form for Client Registration
	class Meta(ClientInfoForm.Meta):
		fields = "__all__"
		widgets = {
			'company_size' : forms.Select(attrs={
				'class' : 'form-control form-control-sm',
			}),
		}

class EmployeeInfoForm(forms.ModelForm):
	# Form to collect or update all client's employees details
	class Meta:
		model = Employee
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
			'designation' : forms.TextInput({
				'class' : 'form-control',
				'placeholder' : 'Designation',
			}),
			'profile_photo' : forms.FileInput(attrs={
				'class' : 'custom-file-input',
				'placeholder' : 'Profile Photo',
			}),
		}

class RegEmployeeForm(EmployeeInfoForm):
	# Form for Client's Employee Registration
	class Meta(EmployeeInfoForm.Meta):
		fields = ['first_name', 'last_name', 'email', 'designation']


class AddJobForm(forms.ModelForm):
	# Form to collect or update all jobs posted by the client
	class Meta:
		model = Job
		fields = '__all__'
		widgets = {
			'title' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Job Title',
			}),
			'location' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Location',
			}),
			'region' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Job Region',
			}),
			'job_type' : forms.Select(attrs={
				'class' : 'form-control form-control-sm',
			}),
			'category' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Category',
			}),
			'tags' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Tags',
			}),
			'description' : forms.Textarea(attrs={
				'class' : 'form-control',
				'placeholder' : 'Job Description',
				'rows' : 2,
			}),
			'salary' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Estimated Salary',
			}),
		}

class ApplicantStatusForm(forms.ModelForm):
	
	class Meta:
		model = Schedule
		fields = '__all__'
		widgets = {
			'screening_status' : forms.Select(attrs={
				'class' : 'form-control from-control-muted form-control-sm',
				'disabled' : 'True',
			}),
			'interview_date' : forms.DateTimeInput(attrs={
					'class' : 'form-control form-control-muted form-control-sm datetimepicker flatpickr',
					'placeholder' : 'Not Scheduled',
					'disabled' : 'True',
			}),
			'interview_status' : forms.Select(attrs={
				'class' : 'form-control form-control-muted form-control-sm',
				'disabled' : 'True',
			}),
			'date_joined' : forms.DateInput(attrs={
				'class' : 'form-control form-control-muted form-control-sm datepicker',
				'placeholder' : 'Not Joined',
				'disabled' : 'True',
			}),
			'progress' : forms.TextInput(attrs={
				'hidden' : 'True',
			})
		}

class SearchForm(forms.Form):
	search = forms.CharField(
		widget = forms.TextInput(attrs={
			'class' : 'form-control',
			'placeholder' : '  Search',
		})
	)

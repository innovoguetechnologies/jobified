from .models import Consultant, Firm
from django.forms import Form, ModelForm, TextInput, EmailInput, Select, IntegerField

class ConsultantInfoForm(ModelForm):
	# Form to collect the details of the firm
	class Meta:
		model = Consultant
		fields = '__all__'
		widgets = {
			'name' : TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Username',
			}),
			'email' : EmailInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Email',
			}),
		}

class ConsultantRegForm(ConsultantInfoForm):
	# Form for consultant registration
	class Meta(ConsultantInfoForm.Meta):
		fields = ['name', 'email',]

class FirmInfoForm(ModelForm):
	# Form to collect all the details fo the firm
	class Meta:
		model = Firm
		fields = '__all__'
		
		widgets = {
			'name' : TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Company',
			}),
			'address' : TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Address',
			}),
			'account_holder' : TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Account Holder',
			}),
			'bank' : TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Bank name & Branch',
			}),
			'account_type' : Select(attrs={
				'class' : 'form-control form-control-sm',
			}),
			'account_no' : TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Account No',
			}),
			'IFSC' : TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'IFSC',
			}),
			'MICR' : TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'MICR',
			}),
			'PAN' : TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'PAN',
			}),
			'website' : TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Website',
			}),
			'GSTIN' : TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'GSTIN',
			}),
			'TAN' : TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'TAN',
			}),
		}

class FirmRegForm(FirmInfoForm):
	# Form to manage the firm's registration
	class Meta(FirmInfoForm.Meta):
		fields = [
			'name', 'address', 'account_holder',
			'bank', 'account_type', 'account_no',
			'IFSC', 'MICR', 'PAN', 'website',
			'GSTIN', 'TAN'
		]

class AddMemberForm(Form):
	# Form to add new members
	phone_no = IntegerField(
		widget = TextInput(attrs={
				'placeholder' : 'Phone No',
				'class' : 'form-control',
				'required' : '',
		}),

	)


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.forms import TextInput, PasswordInput, HiddenInput, ChoiceField, Select
from django import forms

# Custom imports
from .models import User


class RegisterForm(UserCreationForm):
	# The form for recieving the data for authentication details (phone_no and password)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password1'].widget.attrs.update({ 
			'placeholder' : 'Password',
			'class' : 'form-control',
		})
		self.fields['password2'].widget.attrs.update({
			'placeholder' : 'Repeat Password',
			'class' : 'form-control',
		})
		
	class Meta:
		model = User
		fields = ['phone_no', 'country_code']
		widgets = {
			'phone_no' : TextInput(attrs={
				'placeholder' : 'Phone No',
				'class' : 'form-control',
			}),
			'country_code' : Select(attrs={
				'class' : 'form-control',
			}),
		}

class LoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args,**kwargs)
		self.fields['username'].widget.attrs.update({
			'placeholder' : 'Phone Number',
			'class' : 'form-control',
		})
		self.fields['password'].widget.attrs.update({
			'placeholder' : 'Password',
			'class' : 'form-control',
		})

class PasswordChangeForm(PasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args,**kwargs)
		self.fields['old_password'].widget.attrs.update({
			'placeholder' : 'Old Password',
			'class' : 'form-control',
		})
		self.fields['new_password1'].widget.attrs.update({
			'placeholder' : 'New Password',
			'class' : 'form-control',
		})
		self.fields['new_password2'].widget.attrs.update({
			'placeholder' : 'Confirm New Password',
			'class' : 'form-control',
		})

class AddSubordinateForm(forms.Form):
	# Form to add new members
	phone_no = forms.IntegerField(
		widget = forms.TextInput(attrs={
				'placeholder' : 'Phone No',
				'class' : 'form-control',
				'required' : '',
		}),
	)

# Form for OTP Verification
class OTPForm(forms.Form):
	otp = forms.CharField(
		widget = forms.TextInput(attrs={
			'placeholder' : 'Enter the OTP',
			'class' : 'form-control',
			'required' : '',
		}),
	)

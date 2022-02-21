from django import forms
from .models import Poc

class PocInfo(forms.ModelForm):
	# Form for all Poc fields
	class Meta:
		model = Poc
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
		}

class RegPocForm(PocInfo):
	class Meta(PocInfo.Meta):
		exclude = ['profile_photo']

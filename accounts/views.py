"""
	This file contains all the views related to accounts section
"""
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
#from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import RegisterForm, LoginForm, PasswordChangeForm, OTPForm
from consultant.forms import ConsultantRegForm, FirmRegForm
from candidate.forms import CandidateRegForm
from client.forms import ClientRegForm, RegEmployeeForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# Twilio 
from twilio.rest import Client

""" Twilio Verification """

account_sid = 'ACa5af6bace7aefb3a34fe66df99c3f986'
auth_token = '02a382286b830c7a8fef20bed532838f'
verify_service_id = 'VA50512f4ab0d3d210cb38fd20ac947c6f'

# Function to send OTP
def sendOTP(phone_no):
	# Twilio Client instance
	client = Client(account_sid, auth_token)
	
	# Send otp using the twilio api
	verification = client.verify \
		.services(verify_service_id) \
		.verifications \
		.create(to = phone_no, channel = 'sms')
	
	if verification.sid is not None:
		return True
	else:
		return False

# Funciton to verify an OTP
def verifyOTP(country_code, phone_no, otp):
	# Twilio Client instance
	client = Client(account_sid, auth_token)
	
	message = ""
	verified = False
	
	phone_no = "+"+country_code+str(phone_no)
	try:
		verification_check = client.verify \
			.services(verify_service_id) \
			.verification_checks \
			.create(to = phone_no, code=otp)

		if verification_check.status == "approved":
			verified = True
	except Exception as e:
		message = "Error validating OTP, {}".format(e)
		print(message)

	return (verified, message)

""" End Twilio Verification """


def accountrootView(request):
	# A view for accounts app home page.
	# Created for devaloping purpose. Delete when in production
	return render(request, 'accounts/account_root.html')

# View to get the phone no and send the otp
def sendOTPView(request):
	
	# Get phone no from request
	phone_no = request.POST.get('phone_no', None)
	country_code = request.POST.get('country_code', None)
	
	phone_no = '+'+country_code+str(phone_no)
	print(phone_no)
	
	verified = sendOTP(phone_no)
	
	data = {
		'otp_sent' : True,
		'phone_no' : phone_no,
	}
	
	return JsonResponse(data)

def loginView(request, usertype):
	# View for login page
	login_form = LoginForm(request)
	if request.method == 'POST':
		login_form = LoginForm(data = request.POST)
		if login_form.is_valid():
			username = login_form.cleaned_data.get('username')
			password = login_form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None and user.groups.filter(name = usertype).exists():
				login(request, user)
				return redirect(usertype + '_dashboard')
			else:
				messages.error(request, "Invalid username or password.")
		else:
			return HttpResponse('Invalid Form, Try Again')
	context = {
			'login_form' : login_form,
			'usertype'   : usertype,
			'title'      : 'Login',
	}
	return render(request, 'accounts/login.html', context)

def logoutView(request):
	logout(request)
	messages.info(request, "Logged out successfully.")
	return redirect('home')

def candidateRegisterView(request):
	# View for registration page
	#Processing the submitted data
	if request.method == 'POST':
		
		# Populate forms with POST data
		auth_details = RegisterForm(request.POST)
		candidate_details = CandidateRegForm(request.POST)
		otp_form = OTPForm(request.POST)
		country_code = request.POST.get('country_code')
		print(type(country_code))
		# Validate forms
		if (auth_details.is_valid() and candidate_details.is_valid() and otp_form.is_valid()):
			
			# Check OTP Verification
			otp = otp_form.cleaned_data.get('otp')
			country_code = auth_details.cleaned_data.get('country_code')
			phone_no = auth_details.cleaned_data.get('phone_no')
			
			print(phone_no)
			verified, message = verifyOTP(country_code, phone_no, otp)
			
			
			# If OTP Verified
			if verified:
				# Create candidate
				candidate = candidate_details.save(commit=False)
				# Create user
				user = auth_details.save()
				user.save()
				# Adding the user to their respective user group
				candidate_group = Group.objects.get(name = 'candidate')
				user.groups.add(candidate_group)
				# Link user with candidate
				candidate.user = user
				candidate.save()
				# Login and redirect
				login(request, user)
				message = "Howdy "+ candidate.first_name +", Take a second to update your profile."
				messages.success(request, message)
				return redirect('update_candidate_profile')
			else:
				messages.error(request, message)
		else:
			messages.error(request, "Invalid data, Try again..!")
			
	#Creating the forms
	auth_details = RegisterForm()
	candidate_details = CandidateRegForm()
	otp_form = OTPForm()
	context = {
		'auth_details_form' : auth_details,
		'candidate_details_form' : candidate_details,
		'otp_form' : otp_form,
		'title' : "Register as Candidate",
		'usertype' : "candidate",
	}
	return render(request, 'accounts/register_candidate.html', context)

def consultantRegisterView(request):
	# This view manages the consultant registration page.
	#Processing the submitted data
	if request.method == 'POST':
		auth_details = RegisterForm(request.POST)
		consultant_details = ConsultantRegForm(request.POST)
		firm_details = FirmRegForm(request.POST)
		if (auth_details.is_valid() and consultant_details.is_valid() and firm_details.is_valid()):
			print("Forms are valid")

			consultant = consultant_details.save(commit = False)
			# Saving the authentication details
			user = auth_details.save()
			user.save()
			consultant_group = Group.objects.get(name = 'consultant')
			user.groups.add(consultant_group)
			consultant.user = user # Link the user to consultant
			firm = firm_details.save() # Save firm details with no boss
			consultant.firm = firm # Link the firm to the user
			consultant.save() # Save the consultant
			firm.boss = consultant # make the consultant the boss of the firm
			firm.save() # Update changes
			messages.success(request, 'Account created successfully.')
			return redirect('login', usertype='consultant')
		else:
			print('Form not valid')
			messages.success(request, 'Something is wrong')
	# Creating the forms for auth, consultant and firm details.
	auth_details = RegisterForm()
	consultant_details = ConsultantRegForm()
	firm_details = FirmRegForm()
	
	context = {
		'auth_details_form' : auth_details,
		'consultant_details_form' : consultant_details,
		'firm_details_form' : firm_details,
		'title' : "Register as Consultant",
		'usertype' : "consultant",
	}
	return render(request, 'accounts/register_consultant.html', context)

def clientRegisterView(request):
	# This view manages the client registration page.
	#Processing the submitted data
	if request.method == 'POST':
		auth_details = RegisterForm(request.POST)
		employee_details = RegEmployeeForm(request.POST)
		client_details = ClientRegForm(request.POST, request.FILES)
		if (auth_details.is_valid() and employee_details.is_valid() and client_details.is_valid()):
			print("Forms are valid")
			employee = employee_details.save(commit = False)
			user = auth_details.save()
			user.save()
			# Adding the user to their respective group
			client_group, created = Group.objects.get_or_create(name = 'client')
			user.groups.add(client_group)
			boss_group, created = Group.objects.get_or_create(name = 'boss')
			user.groups.add(boss_group)
			
			employee.user = user
			employee.company = client_details.save()
			employee.save()
			messages.success(request, 'Account created successfully.')
			return redirect('login', usertype='client')
		else:
			print('Form not valid')
			messages.success(request, 'Something is wrong')
	# Creating the forms for auth, consultant and firm details.
	auth_details = RegisterForm()
	employee_details = RegEmployeeForm()
	client_details = ClientRegForm()
	
	context = {
		'auth_details_form' : auth_details,
		'employee_details_form' : employee_details,
		'client_details_form' : client_details,
		'title' : "Register as Client",
		'usertype' : "client",
	}
	return render(request, 'accounts/register_client.html', context)

def successView(request):
	return render(request, 'accounts/accounts_success.html')

@login_required
def changePasswordView(request):
	data = dict()
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			data['form_is_valid'] = True
			data['message'] = '<div class="alert alert-success alert-dismissible fade show" role="alert"><span class="alert-icon"><i class="ni ni-like-2"></i></span><span class="alert-text">Password Changed Successfully</span><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
		else:
			data['message'] = '<div class="alert alert-danger" role="alert">Invalid Credentials! Try again</div>'
	else:
		form = PasswordChangeForm(request.user)
		data['html_form'] = render_to_string('accounts/change_password.html', { 'form' : form }, request = request)
	return JsonResponse(data)

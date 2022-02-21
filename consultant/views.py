# Consultant's WebView Configurations

# Built-in feature import
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import random
from string import ascii_letters, digits

# User defined feature import
from .models import Firm, Consultant
from .forms import ConsultantRegForm, AddMemberForm
from accounts.models import User


@login_required
def dashboardView(request):
	consultant = request.user.consultant
	context = {
		'consultant' : consultant, 
	}
	return render(request, 'consultant/dashboard.html', context = context)

@login_required
def addMemberView(request):
	# Form to add new member
	data = dict()
	if request.method == 'POST' and request.is_ajax():
		print("inside save function")
		auth_details = AddMemberForm(request.POST)
		consultant_details = ConsultantRegForm(request.POST)
		# Creating a random password
		random_password = ''.join((random.choice(ascii_letters + digits) for i in range(9)))
		if (auth_details.is_valid() and consultant_details.is_valid()):
			print("Forms are valid")
			phone_no = auth_details.cleaned_data['phone_no']
			print(random_password)
			consultant = consultant_details.save(commit = False)
			# Create a user with random password and link to consultant
			consultant.user = User.objects.create_user(phone_no = phone_no, usertype = 2, password = random_password) 
			consultant.firm = request.user.consultant.firm # Link the firm of the boss to consultant
			consultant.save() # Save the consultant
			data['form_is_valid'] = True
			#Updating the members list
			members = Consultant.objects.filter(firm = request.user.consultant.firm)
			data['html_member_list'] = render_to_string('consultant/part_members.html', {
				'members': members,
			})
		else:
			data['form_is_valid'] = False
	else:
		auth_details = AddMemberForm()
		consultant_details = ConsultantRegForm()
	context = {
		'auth_details_form' : auth_details,
		'consultant_details_form' : consultant_details,
	}
	data['html_form'] = render_to_string('consultant/add_member.html', context, request = request)
	return JsonResponse(data)

@login_required
def listMembersView(request):
	# Returns the consultant members list and operations.
	members = Consultant.objects.filter(firm = request.user.consultant.firm)
	context = {
		'members' : members,
	}
	return render(request, 'consultant/members.html', context = context)

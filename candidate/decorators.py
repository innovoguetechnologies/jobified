from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

# A decorator to check if the user is candidate or not
def candidate_required(function):
	def wrap(request, *args, **kwargs):
		if request.user.groups.filter(name = 'candidate').exists():
			return function(request, *args, **kwargs)
		else:
			logout(request)
			messages.error(request, "Permission Denied. You need to login as a candidate")
			return redirect('login', usertype='candidate')
	return wrap

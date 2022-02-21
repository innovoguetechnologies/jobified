from django.contrib.auth import logout
from django.shortcuts import redirect

# A decorator to check if the user is company staff or not
def company_required(function):
	def wrap(request, *args, **kwargs):
		if request.user.groups.filter(name = 'company').exists():
			return function(request, *args, **kwargs)
		else:
			logout(request)
			return redirect('login', usertype='company')
	return wrap

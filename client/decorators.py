from django.contrib.auth import logout
from django.shortcuts import redirect

# A decorator to check if the user is client or not
def client_required(function):
	def wrap(request, *args, **kwargs):
		if request.user.groups.filter(name = 'client').exists():
			return function(request, *args, **kwargs)
		else:
			logout(request)
			return redirect('login', usertype='client')
	return wrap
	
# A decorator to check if the user is boss or not
def boss_required(function):
	def wrap(request, *args, **kwargs):
		if request.user.groups.filter(name = 'boss').exists():
			return function(request, *args, **kwargs)
		else:
			logout(request)
			return redirect('login', usertype='client')
	return wrap

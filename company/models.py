from django.db import models
from django.conf import settings

class Poc(models.Model):
	first_name = models.CharField(
		max_length = 50,
		blank = False,
		help_text = "First name of the employee",
		verbose_name = "First Name",
	)
	last_name = models.CharField(
		max_length = 50,
		blank = False,
		help_text = "Last name of the employee",
		verbose_name = "Last Name",
	)
	email = models.EmailField(
		verbose_name = "Email",
		help_text = "Email id of the employee.",
		unique = True,
	)
	profile_photo = models.ImageField(
		verbose_name = "Profile Photo",
		help_text = "Profile Photo of the POC",
		blank = False,
		null = True,
	)
	
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete = models.CASCADE,
		editable = False
	)

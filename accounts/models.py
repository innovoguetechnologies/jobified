from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from . import choices

class UserManager(BaseUserManager):
	# Creates a regular user
	def create_user(self, country_code, phone_no, password = None):
		# Checking for email and username
		if not phone_no:
			raise ValueError("Enter a valid phone number")
		if not country_code:
			raise ValueError("Enter a valid country code")

		# Adding the data to the model and registering
		user = self.model(
			country_code = country_code,
			phone_no = phone_no,
			password = password,
		)

		user.set_password(password)
		user.save(using = self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin):
	"""		Custom User model - Common to every user	 """
	country_code = models.CharField(
		max_length=6,
		choices = choices.country_codes,
		verbose_name = "Country code",
		null = False,
		blank = False,
		default = 91,
	)
	phone_no = models.BigIntegerField(
		primary_key = True,
		verbose_name = "Phone Number",
		unique = True,
		null = False,
		blank = False,
		help_text = "Please enter a phone number."
	)
	# PasswordField is provided by the AbstractBaseUser class
	# LastLoginField is provided by the AbstractBaseUser class
	date_joined = models.DateTimeField(
		verbose_name = 'Date joined',
		auto_now_add = True,
	)
	
	last_login = models.DateTimeField(
		verbose_name = 'Last login',
		auto_now = True,
	)
	
	USERNAME_FIELD = 'phone_no'
	
	objects = UserManager()
	
	# Methods
	def __int__(self):
		return self.phone_no


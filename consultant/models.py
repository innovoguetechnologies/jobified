from django.db import models
from django.conf import settings

class Firm(models.Model):
	name = models.CharField(
		max_length = 100,
		help_text = "Name of the consultant firm.",
		blank = True,
	)
	address = models.TextField(
		help_text = "The address of the firm, as in bank and official records",
		blank = False,
	)
	
	account_holder = models.CharField(
		max_length = 100,
		help_text = "The name of the bank account holder",
		blank = False,
	)
	account_no = models.CharField(
		max_length = 34,
		blank = False,
	)
	bank = models.TextField(
		help_text = "The name and branch of the bank.",
		blank = False,
	)
	account_type_choices = [
		('SA' , 'Savings'),
		('CU' , 'Current'),
		('CA' , 'Cash'),
		('DA' , 'Draft'),
	]
	account_type = models.CharField(
		verbose_name = "Account Type : ",
		max_length = 3,
		choices = account_type_choices,
		help_text ="Type of the bank account.",
		blank = False,
		default = 'SA',
	)
	IFSC = models.CharField(
		max_length = 11,
		help_text = "IFSC code of the bank",
		blank = False,
	)
	MICR = models.CharField(
		max_length = 9,
		help_text = "MICR of the cheque.",
		blank = False,
		unique =True,
	)
	PAN = models.CharField(
		max_length = 10,
		help_text = "PAN number of the account holder.",
		blank = False,
		unique =True,
	)
	website = models.CharField(
		max_length = 100,
		help_text = "Website of the firm.",
		blank = True
	)
	GSTIN = models.CharField(
		max_length = 15,
		help_text = "GSTIN number of the account holder.",
		blank = False,
		unique =True,
	)
	TAN = models.CharField(
		max_length = 10,
		help_text = "TAN number of the account holder.",
		blank = False,
		unique =True,
	)
	
	boss = models.OneToOneField('Consultant', on_delete = models.CASCADE, editable = False, related_name = 'boss', default = None)

class Consultant(models.Model):
	name = models.CharField(max_length = 100)
	email = models.EmailField(
		help_text = "Email id of the consultant.",
		unique = True,
	)
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete = models.CASCADE,
		editable = False,
	)
	firm = models.ForeignKey(Firm, on_delete = models.CASCADE, editable = False)

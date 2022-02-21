from django import template

register = template.Library()

@register.filter
def is_user_type(user, usertype):
	if user.groups.filter(name = usertype).exists():
		print("True")
		return True
	else:
		return False

@register.filter
def get_exp_month(exp):
	year = int(exp)
	month = round((exp - year) * 12)
	return month

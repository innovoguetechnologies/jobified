Project Name        : JobGate India
Author              : Amal Sebastian
Email               : amalsebastian.dev@gmail.com
                      amalsebastian.official@gmail.com

Company             : Innovogue Technologies

    This project aims to create an environment for consultants, candidate and companies to meet and fulfill their needs of employment.

Conventions :

    The project uses bootstrap theme developed by Creative-Tim and modified by us (Innovogue Technologies).

Main Business Model Entities :

1. Candidate
    The jobseeker.
    css-class : bg-candidate

2. Consultant
    The mass candidate uploader.
    css-class : bg-consultant

3. Client
    The company that needs employees and post vaccancies.
    css-class : bg-client

4. Company
    The company JobGate.
    css-class : bg-company
    
Remarks :

	There are mainly 5 groups used in this project all of which where created in the shell.
	1. candidate
	2. client
	3. consultant
	4. company
	5. boss (Which enables the user to view their subordinates, and manage company / firm)
	
	Code :
		from django.contrib.auth.models import Group
		group_name = Group.objects.get_or_create(name = 'group_name')
	where group_name is the name of the group

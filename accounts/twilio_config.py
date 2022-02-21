""" Twilio config File """
from twilio.rest import Client

account_sid = 'ACa5af6bace7aefb3a34fe66df99c3f986'
auth_token = '02a382286b830c7a8fef20bed532838f'
verify_service_id = 'VA50512f4ab0d3d210cb38fd20ac947c6f'

client = Client(account_sid, auth_token)

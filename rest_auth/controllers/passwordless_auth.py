from http import HTTPStatus

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Router
from twilio.rest import Client

from config.utils.common_utils import response
from rest_auth.models import PasswordlessAccountManager, CallbackToken
from rest_auth.permissions import get_token_for_user, PasswordlessAuthorization
from rest_auth.schemas import MessageOut
from rest_auth.schemas.passwordless_account_schemas import PasswordlessAuthMessageOut, PasswordlessAuthIn, \
    PasswordlessAuthConfirmationIn, PasswordlessAccountOut, PasswordlessUpdateIn

User = PasswordlessAccountManager

PASSWORDLESS_TOKEN_EXPIRE_TIME = getattr(settings, 'PASSWORDLESS_TOKEN_EXPIRE_TIME', 120)  # 900 seconds
TWILIO_ACCOUNT_SID = getattr(settings, 'TWILIO_ACCOUNT_SID', 'AC80921502ecb4c33c95e735e9f4f186b7')
TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', 'a8f230dfcd4d9c7a3503a2b33f4d63f6')
TWILIO_ACCOUNT_FROM = getattr(settings, 'TWILIO_ACCOUNT_FROM', '+13346978007')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

passwordless_auth = Router(tags=['Passwordless Auth'])


def validate_token_age(callback_token):
    """
        Returns True if a given token is within the age expiration limit.
        """
    try:
        token = CallbackToken.objects.get(key=callback_token, is_active=True)
        seconds = (timezone.now() - token.created).total_seconds()
        token_expiry_time = PASSWORDLESS_TOKEN_EXPIRE_TIME

        print("token_expiry_time", token_expiry_time)

        if seconds <= token_expiry_time:
            return True
        # Invalidate our token.
        token.is_active = False
        token.forced_expired = True
        token.save()
        return False

    except CallbackToken.DoesNotExist:
        # No valid token.
        return False


@passwordless_auth.post('/entry',
                        auth=None,
                        response={200: PasswordlessAuthMessageOut})
def entry(request, user_in: PasswordlessAuthIn):
    phone_number = user_in.phone_number

    try:
        # if user is registered
        user = User.objects.get(phone_number=phone_number)

        # if user exists, then generate a key for him
        key = CallbackToken.objects.create(user=user)

        print(f'{key} -------------------------')

        # now, send the code to the user via SMS
        sms = f'{key} is your verification code to login to the shop.'

        # message = client.messages.create(
        #     body=sms,
        #     from_=TWILIO_ACCOUNT_FROM,
        #     to=phone_number
        # )

        verify_sms_response = {
            'status': 'success',
            'message': f'Verification code has been sent successfully',
            'token': None,
        }

        return response(HTTPStatus.OK, verify_sms_response)

    except User.DoesNotExist:
        # create new user
        data = {
            'phone_number': phone_number,
        }

        user = User(phone_number=phone_number)
        user.save()

        # generate a key
        key = CallbackToken.objects.create(user=user)

        # now, send the code to the user via SMS
        sms = f'{key} is your verification code to create account and login to the shop.'

        # message = client.messages.create(
        #     body=sms,
        #     from_=TWILIO_ACCOUNT_FROM,
        #     to=phone_number
        # )

        verify_sms_response = {
            'status': 'success',
            'message': f'Verification code has been sent successfully',
            'token': None,
        }

        return response(HTTPStatus.OK, verify_sms_response)


@passwordless_auth.post('/confirm',
                        auth=None,
                        response={200: PasswordlessAuthMessageOut, 400: PasswordlessAuthMessageOut})
def confirm(request, confirmation_in: PasswordlessAuthConfirmationIn):
    phone_number = confirmation_in.phone_number
    verification_code = confirmation_in.verification_code

    try:
        user = User.objects.get(
            phone_number=phone_number,
        )

        try:
            code = CallbackToken.objects.get(key=verification_code, is_active=True)

            # make sure the code belongs to the correct user
            if code.user != user:
                verify_sms_response = {
                    'status': 'error',
                    'token': None,
                    'message': 'This verification code is not correct. please try again.',
                }

                return response(HTTPStatus.BAD_REQUEST, verify_sms_response)

            # make sure the code is not expired
            is_valid = validate_token_age(code)

            if is_valid:
                # mark the code as used
                code.is_active = False
                code.is_used = True
                code.date_used = timezone.now()
                code.save()

                # generate auth token
                token = get_token_for_user(user, 'PU')

                verify_sms_response = {
                    'status': 'success',
                    'token': token,
                    'message': 'User authentication successful',
                }

                return response(HTTPStatus.OK, verify_sms_response)

            verify_sms_response = {
                'status': 'error',
                'token': None,
                'message': 'User authentication failed, verification code expired',
            }
            return response(HTTPStatus.BAD_REQUEST, verify_sms_response)
        except CallbackToken.DoesNotExist:
            verify_sms_response = {
                'status': 'error',
                'token': None,
                'message': 'Code does not exist',
            }
            return response(HTTPStatus.BAD_REQUEST, verify_sms_response)

    except User.DoesNotExist:
        verify_sms_response = {
            'status': 'error',
            'token': None,
            'message': 'You are not registered',
        }
        return response(HTTPStatus.BAD_REQUEST, verify_sms_response)


@passwordless_auth.get('/me',
                       auth=PasswordlessAuthorization(),
                       response={200: PasswordlessAccountOut, 400: MessageOut})
def me(request):
    try:
        user = request.auth.get('user')
    except AttributeError:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'token missing'})
    return response(HTTPStatus.OK, user)


@passwordless_auth.put('/me',
                       auth=PasswordlessAuthorization(),
                       response={200: PasswordlessAccountOut, 400: MessageOut})
def update_me(request, user_in: PasswordlessUpdateIn):
    User.objects.filter(phone_number=request.auth.get('user')).update(**user_in.dict())
    # print(user)
    user = get_object_or_404(User, phone_number=request.auth.get('user'))
    # print(user)
    if not user:
        return response(HTTPStatus.BAD_REQUEST, data={'message': 'something went wrong'})
    return response(HTTPStatus.OK, user)

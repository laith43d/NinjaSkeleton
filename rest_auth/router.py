from ninja import NinjaAPI

from rest_auth.controllers.passwordless_auth import passwordless_auth

api = NinjaAPI(
    version='1.0.0',
    title='Passwordless client API v1',
    description='API documentation for PayGate Mobile Clients',
)

api.add_router('/auth', passwordless_auth)


from django.contrib.auth.models import UserManager, AbstractUser

from config.utils.common_models import Entity


# class UserNameAccountManager(UserManager):
#     def get_by_natural_key(self, username):
#         case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
#         return self.get(**{case_insensitive_username_field: username})
#
#
# class UserNameAccount(AbstractUser, Entity):
#     objects = UserNameAccountManager()

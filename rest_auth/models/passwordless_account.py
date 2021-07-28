import uuid

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from config.utils.common_models import Entity
from config.utils.common_utils import custom_key_generator


class PasswordlessAccountManager(models.Manager):
    def create_user(
            self,
            phone_number,
            email=None,
    ):
        if not phone_number:
            raise ValueError("Users must have an phone number!")

        user_obj = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email)
        )

        user_obj.save(using=self._db)
        return user_obj


class PasswordlessAccount(Entity):
    phone_number = models.CharField(db_index=True, max_length=100, verbose_name='phone number', unique=True)
    email = models.EmailField(db_index=True, verbose_name='email address', max_length=255, blank=True,
                              null=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)  # can login or not

    objects = PasswordlessAccountManager()

    def __str__(self):
        return f'{self.phone_number}'

    def get_full_name(self):
        # The user is identified by their phone_number
        return f'{self.name}'.replace('None', '')

    def get_short_name(self):
        # The user is identified by their phone_number
        return self.phone_number

    @property
    def is_active(self):
        return self.active


class CallbackTokenManger(models.Manager):
    def active(self):
        return self.get_queryset().filter(is_active=True)

    def inactive(self):
        return self.get_queryset().filter(is_active=False)


class CallbackToken(models.Model):
    """
    Description:This is going to be the handle all the tokens sent to the users.\n
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('rest_auth.PasswordlessAccount', on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)

    is_invalidated = models.BooleanField(default=False)
    '''When a user creates a key all their previous active keys are
           invalidated.This way only one key is active.
           We want to know whether the key was invalidated and when used
           it is captured in the is_used field.
    '''

    key = models.CharField(max_length=10, db_index=True, unique=True, blank=True)  # length is 4 digits

    is_used = models.BooleanField(default=False)

    date_used = models.DateTimeField(blank=True, null=True)

    forced_expired = models.BooleanField(default=False)  # whether the code was forced to expire
    expires = models.IntegerField(default=7)  # 7 Days #How long a code should stay before expiring
    updated = models.DateTimeField(auto_now=True, editable=False)

    objects = CallbackTokenManger()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.key)

    def get_absolute_url(self):
        pass


def key_pre_save_receiver(sender, instance, *args, **kwargs):
    """
    Description:Create a key for every saved instance.\n
    """
    if not instance.key:
        instance.key = custom_key_generator(instance)


pre_save.connect(key_pre_save_receiver, sender=CallbackToken)


@receiver(post_save, sender=CallbackToken)
def pre_save_invalidate_previous_keys_receiver(sender, instance, created, *args, **kwargs):
    """
    Description:Invalidates all previously issued active keys.
    """
    if not created:
        return
    active_keys = None
    if isinstance(instance, CallbackToken):
        active_keys = CallbackToken.objects.active().filter(user=instance.user).exclude(id=instance.id)

    # Invalidate keys
    if active_keys:
        print("active_keys", active_keys)
        for token in active_keys:
            token.is_active = False
            token.is_invalidated = True

            token.save()

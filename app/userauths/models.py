

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    phone = models.CharField(max_length=45, unique=True)
    email = models.CharField(max_length=80, unique=True)
    image = models.ImageField(upload_to="image")

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email", "username", "first_name"]

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _("Users")
        db_table = "users_db"

    def __str__(self):
        return f"{str(self.username)} + {str(self.email)}"


class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)  # +234 (456) - 789
    subject = models.CharField(max_length=200)  # +234 (456) - 789
    message = models.TextField()

    class Meta:
        verbose_name = _("Contact Us")
        verbose_name_plural = _("Contact Us")
        db_table = "contact_us_db"

    def __str__(self):
        return self.full_name


class Message(models.Model):
    message = models.CharField(max_length=150)

    class Meta:
        ordering = ['-id']
        verbose_name = _('Message')
        verbose_name_plural = _("Messages")
        db_table = 'messages_db'

    def __str__(self) -> str:
        return self.message


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    verified = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.full_name} - {self.bio}"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

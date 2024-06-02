from modeltranslation.translator import TranslationOptions, register

from .models import *


@register(User)
class UserTranslation(TranslationOptions):
    fields = ('first_name', 'last_name', )
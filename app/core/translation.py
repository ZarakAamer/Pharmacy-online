from modeltranslation.translator import TranslationOptions, register

from .models import *


@register(BigBanner)
class BigBannerTranslationOptions(TranslationOptions):
    fields = ("name", "user_catcher", "short_line")


@register(SideBanner)
class SideBannerTranslationOptions(TranslationOptions):
    fields = ("type", "user_catcher")


@register(MainCategory)
class MainCategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("title", "description", "specifications")


@register(Prescription)
class PrescriptionTranslationOptions(TranslationOptions):
    fields = ("subject", "prescription")


@register(Advices)
class AdvicesTranslationOptions(TranslationOptions):
    fields = ("title", "description", "advice")


@register(Doctor)
class DoctorTranslationOptions(TranslationOptions):
    fields = ("name", "details", "specialty")


@register(Consultation)
class ConsultationTranslationOptions(TranslationOptions):
    fields = ("subject", "content")


@register(Insurance)
class InsuranceTranslation(TranslationOptions):
    fields = ("subject", "prescription", "company", "insurance_card", "done")


@register(Locations)
class LocationsTranslationOptions(TranslationOptions):
    fields = ("city_name", "details")


@register(Bank)
class BankInfoTranslationOptions(TranslationOptions):
    fields = ("instructions", "account_info")


@register(AboutUs)
class AboutUsTranslationOptions(TranslationOptions):
    fields = ("address", "description")

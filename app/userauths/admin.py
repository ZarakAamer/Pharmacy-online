from django.contrib import admin
from userauths.models import ContactUs, User, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    ...


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "phone"]


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "subject"]


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'full_name', 'bio', 'phone']


admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
